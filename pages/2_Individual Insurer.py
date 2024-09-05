import pandas as pd
import numpy as np
import openpyxl
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, ColumnsAutoSizeMode,ExcelExportMode
from grid_options import get_grid_options
from Chatbot import chatwithdata

#configuration
st.set_page_config(layout = "wide")
color1 = "#A7AED2"
color_zurich = '#5B769D'
color_pie_chart = ['#3C4D68', '#5B769D', '#6C88B2', '#92ABC8', '#ACC2D8', '#B9C0CA', '#C3BFC1', '#CCBEB7', '#C0ACA5', '#B49993', '#CCA3A3']
color_stacked_bar = ['#3C4D68', '#6C88B2', '#A9B5C6', '#C8CCD0', '#E6E2DA', '#B5ABB6', '#9D8FA4', '#9E8F94', '#9E8F84', '#A7998F', '#96918E', '#85898D', '#62798B']

#prepare data: G19 (overall); G20 & G21 (break down)
df_uw_all = pd.read_csv('Data/df_clean_G19_18to22.csv')
df_uw_breadown_G20 = pd.read_csv('Data/df_clean_G20_18to22.csv')
df_uw_breadown_G21 = pd.read_csv('Data/df_clean_G21_18to22.csv')
df_uw_breakdown = pd.merge(df_uw_breadown_G20, df_uw_breadown_G21, on = ['Insurer', 'FY', 'Category'], how = 'inner')
df_uw_breakdown = df_uw_breakdown[['Insurer', 'FY', 'Category', 'Gross Premium', 'Net Premium', 'Gross Claims Paid', 'Net Claims Paid']]
df_uw_breakdown['FY'] = df_uw_breakdown['FY'].astype(str)

FY_lst = list(set(df_uw_all['FY'].to_list()))
Insurer_lst = list(set(df_uw_all['Insurer'].to_list()))
Metircs_lst = df_uw_all.drop(['Insurer', 'FY'], axis = 1).columns  
Metrics_lst_target = ['Gross Premium', 'Net Premium', 'Gross Claims Paid', 'Net Claims Paid']

#Insurer Comparison
with st.container():
    col1, col2 = st.columns(2)
    with col1: 
        select_FY = st.selectbox("Select Financial Year", FY_lst)
    with col2: 
        select_metrics = st.selectbox("Select Metrics", Metrics_lst_target)
    df_select_FY = df_uw_all[df_uw_all['FY'] == select_FY].sort_values(by = select_metrics, ascending = False)
    df_top10 = df_select_FY[:10][['Insurer', select_metrics]].sort_values(by = select_metrics, ascending = True)
    df_left = df_select_FY[10:][['Insurer', select_metrics]]
    df_left_all = pd.DataFrame({'Insurer': 'Sum of Rest Insurers', select_metrics: df_left[select_metrics].sum()}, index = [0])
    df_final = pd.concat([df_top10, df_left_all]).sort_values(by = 'Insurer', ascending=False)
    Insurer_lst2 = df_final['Insurer'].to_list()
    top10_list = df_top10['Insurer'].to_list()
    pull_dict = {}
    for insurer in Insurer_lst2:
        if insurer == 'Zurich Insurance':
            pull_dict[insurer] = 0.15
        else:
            pull_dict[insurer] = 0
            
    col3, col4 = st.columns(2)
    with col3:
        fig1 = go.Figure(
            data = [
                go.Pie(
                    labels = Insurer_lst2,
                    values = list(map(lambda insur: df_final.loc[df_final['Insurer'] == insur, select_metrics].values[0], Insurer_lst2)),
                    pull=list(map(lambda insur: pull_dict[insur], Insurer_lst2))
                )
            ]
        )
        fig1.update_traces(hoverinfo = 'label+value+percent', textinfo = 'percent', marker = dict(colors = color_pie_chart))
        fig1.update_layout(
        margin=dict(t=30, b=20, l=20, r=20),
        width=400,
        height=400, legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.8,
            xanchor="center",
            x=0.5
        ), title_text = f"{select_FY} {select_metrics} market share ($'000)")
        st.plotly_chart(fig1)
    
    with col4: 
        colors_bar = [color1] * len(top10_list)
        if 'Zurich Insurance' in top10_list:
            colors_bar[top10_list.index('Zurich Insurance')] = color_zurich
        fig2 = go.Figure(
            go.Bar(
                x = list(map(lambda insur: df_top10.loc[df_top10['Insurer'] == insur, select_metrics].values[0], top10_list)),
                y = top10_list,
                orientation='h',
                marker_color = colors_bar
            )
        )
        fig2.update_layout(
        margin=dict(t=30, b=20, l=20, r=20),
        width=400,
        height=400, title_text = f"{select_FY} {select_metrics} market ranking ($'000)")
        st.plotly_chart(fig2)
    
#Individual performance trend
if "select_insurer" not in st.session_state:
    st.session_state.select_insurer = 'Zurich Insurance'  # Set a default value for the insurer
if "select_metrics_individual" not in st.session_state:
    st.session_state.select_metrics_individual = 'Gross Premium'  # Set a default value for the metrics

with st.container():
    col1, col2 = st.columns(2)
    with col1: 
        select_insurer = st.selectbox("Select Insurer", Insurer_lst, key="select_insurer")
    with col2: 
        select_metrics_individual = st.selectbox("Select Metrics", Metircs_lst)
               
    #If select these 4 metrics, then can break down
    if select_metrics_individual in ('Gross Premium', 'Net Premium', 'Gross Claims Paid', 'Net Claims Paid'):    
        df_uw_bd = df_uw_breakdown[df_uw_breakdown['Category']!='Total']
        df_select_insurer_bd = df_uw_bd[df_uw_bd['Insurer'] == select_insurer].sort_values(by = ['FY', select_metrics_individual], ascending = [True, False])
        fig3 = px.bar(
                    df_select_insurer_bd,
                    x = 'FY',
                    y = select_metrics_individual,
                    color = 'Category',
                    color_discrete_sequence = color_stacked_bar
                )
        fig3.update_layout(title_text = f"{select_insurer} {select_metrics_individual} ($'000)", legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5
            ))
        st.plotly_chart(fig3, use_container_width=True) 
    
    #otherwise show overall value    
    else:
        df_select_insurer = df_uw_all[df_uw_all['Insurer'] == select_insurer]
        fig3 = go.Figure(
            data = go.Bar(
                x = FY_lst,
                y = list(map(lambda fy: df_select_insurer.loc[df_select_insurer['FY'] == fy, select_metrics_individual].values[0], FY_lst)),
                marker_color = color1
            )
        )
        fig3.update_layout(title_text = f"{select_insurer} {select_metrics_individual} ($'000)")
        st.plotly_chart(fig3, use_container_width=True)
                   
#expander
with st.expander('Individual Insurer UW Data'):
    ag = AgGrid(
        df_uw_all,
        gridOptions = get_grid_options(df_uw_all, selection_mode = "multiple"),
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        enable_quicksearch=True,
        excel_export_mode=ExcelExportMode.MANUAL)
with st.expander('Individual Insurer UW Data Break Down'):
    ag = AgGrid(
        df_uw_bd,
        gridOptions = get_grid_options(df_uw_bd, selection_mode = "multiple"),
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        enable_quicksearch=True,
        excel_export_mode=ExcelExportMode.MANUAL)
    
st.title('Chat with Insurer Data Here:')
chatwithdata(df_uw_all)
    
    





