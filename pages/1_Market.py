import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import base64
import os
from st_aggrid import AgGrid, ColumnsAutoSizeMode,ExcelExportMode
from grid_options import get_grid_options
from Chatbot import chatwithdata


df_market_G1 = pd.read_csv('Data/df_clean_G1_18to22.csv')
df_market_G1 = df_market_G1.rename(columns={col: f"{col}($m)" for col in df_market_G1.columns if col not in ['FY', 'Category']})
df_market_G6810 = pd.read_csv('Data/df_clean_G6_G8_G10_18to22.csv')
df_market_all = pd.merge(df_market_G1, df_market_G6810, on = ['FY', 'Category'], how = 'inner').sort_values(by=['FY', 'Category'])
df_market_all = df_market_all[['FY', 'Category'] + [col for col in df_market_all.columns if col not in ['FY', 'Category']]]
color_stacked_bar = ['#3C4D68', '#6C88B2', '#A9B5C6', '#C8CCD0', '#E6E2DA', '#B5ABB6', '#9D8FA4', '#9E8F94', '#9E8F84', '#A7998F']


metrics_list = df_market_G1.drop(['FY', 'Category'], axis = 1).columns
category_list = ['Total', 'Accident & Health', 'Motor Vehicle', 'Aircraft', 'Ships', 'Goods in Transit', 'Property Damage', 'General Liability', 'Pecuniary Loss', 'Non-Proportional Treaty Reinsurance', 'Proportional Treaty Reinsurance']
ratio_metrics_list = df_market_G6810.drop(['FY', 'Category'], axis = 1).columns

with st.container():
    col1, col2 = st.columns(2)
    with col1: 
        select_metrics = st.selectbox("Select Metrics", metrics_list)

        df_market_bd = df_market_G1[df_market_G1['Category']!='Total'].sort_values(by=['FY', select_metrics], ascending=[True, False])
        fig = px.bar(
                    df_market_bd,
                    x = 'FY',
                    y = select_metrics,
                    color = 'Category',
                    color_discrete_sequence = color_stacked_bar
                )
        fig.update_layout(title_text = f"Market {select_metrics} Trend", legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5
            ))
        st.plotly_chart(fig, use_container_width=True) 

    with col2:
        col3, col4 = st.columns(2)
        with col3: 
            select_ratio_metrics = st.selectbox('Select Ratio Metrics', ratio_metrics_list)
        with col4:
            select_category = st.selectbox('Select Category', category_list)
        
        # df_market_ratio = df_market_G6810[df_market_G6810['Category'] == select_category]
        # fig2 = px.line(df_market_ratio, x = 'FY', y = select_ratio_metrics, markers = True)
        # fig2.update_layout(yaxis = dict(range=[0,100]))
        # st.plotly_chart(fig2, use_container_width = True)

        df_market_ratio = df_market_G6810[df_market_G6810['Category'] == select_category]

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_market_ratio['FY'],
            y=df_market_ratio[select_ratio_metrics],
            mode='lines+markers+text',
            text=df_market_ratio[select_ratio_metrics].round(2).astype(str),
            textposition='top center',
            marker=dict(
                size=10,
                color='#1f77b4'
            )
        ))

        fig2.update_traces(textfont_size=12, textfont_color='#1f77b4')
        fig2.update_layout(
            yaxis=dict(range=[0, 100]),
            title=f"{select_category} {select_ratio_metrics} Trend",
            xaxis_title='FY',
            yaxis_title=select_ratio_metrics,
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="black"
            )
        )

        st.plotly_chart(fig2, use_container_width=True)

    with st.expander('Market Data'):
        ag = AgGrid(
            df_market_all,
            gridOptions = get_grid_options(df_market_all, selection_mode = "multiple"),
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
            enable_quicksearch=True,
            excel_export_mode=ExcelExportMode.MANUAL
            )
        
st.title("Chat with Market Data Here:")
chatwithdata(df_market_all)