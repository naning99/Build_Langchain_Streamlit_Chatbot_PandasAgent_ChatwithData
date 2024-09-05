import pandas as pd
from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_openai import (ChatOpenAI, AzureChatOpenAI)
import os
import streamlit as st
import openai

load_dotenv()

def chatwithdata(df):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    azure_endpoint = os.getenv("endpoint")
    if ("messages" not in st.session_state):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    elif (st.session_state.messages is None):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="What is this data about?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        llm = AzureChatOpenAI(
            model_name="gpt-4o-20240513-standard",
            api_key = openai_api_key,
            api_version='2024-02-01',
            azure_endpoint=azure_endpoint,
            temperature = 0
        )

        pandas_df_agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            allow_dangerous_code=True,
            agent_executor_kwargs={"handle_parsing_errors": "Parsing errror, processing...Please wait"}
        )

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)

    def reset_conversation():
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]
    st.button('Reset Chat', on_click=reset_conversation)
    
