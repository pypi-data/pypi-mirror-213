"""
- Title:            Hybrid Assistant UI functions (https://streamlit.io/)
- Project/Topic:    Smart Data Science scenario
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress
"""


from typing import Any

# import numpy as np
import pandas as pd
import streamlit as st

from smart_data_science import logger
from smart_data_science.llm.assistant import HybridAssistant

log = logger.get_logger(__name__)

DEFAULT_PROMPT_PLOT = "Colored Violin plot of the target by a relevant categorical variable"

DEFAULT_PROMPT_DATA_PROCESSING = ""
# "Generate new variable or variables that could be better related to the target via \
# Feature Engineering. Important: Do not use the target variable to create any new feature \
# (that would result in target leakage),  and do not expand the categories. \
# Return the extended table with all the original and new variables"


DEFAULT_PROMPT_CONTEXT_ANALYSIS = "Structured summary of the context you have also showing some statistics about the \
target and the prediction if you already know them. Do not include ML params"

SESSION_STATE_VARIABLES = [
    "assistant",
]
for st_var in SESSION_STATE_VARIABLES:
    if st_var not in st.session_state:
        st.session_state[st_var] = None


def create_assistant(df: pd.DataFrame, topic_context=None, model=None, debug=False) -> HybridAssistant:
    """Build the Scenario & its session state variable
    This function must be called at the beginning of the app and
    after a new file (definitions, plan ...) is uploaded
    Args:
        df (pd.DataFrame): Default Dataframe to be used by the assistant
    Returns:
        HybridAssistant: Hybrid Assistant
    """
    assistant = HybridAssistant(df=df, topic_context=topic_context, model=model, debug=debug)
    st.session_state["assistant"] = assistant
    log.debug("Hybrid Assistant Ready")
    return assistant


def basic_assistant(df: pd.DataFrame) -> None:
    """Display the Basic Hybrid Assistants in the UI
    Args:
        df (pd.DataFrame): Dataframe to be used by the assistant
    """

    assistant = st.session_state["assistant"]
    assistant.set_data(df)

    st.markdown("## Assisted Plot")
    request = st.text_area("**Describe the plot desired**", value=DEFAULT_PROMPT_PLOT)
    if st.button("Send Plot Request"):
        fig = assistant.request_plot(request)
        if fig is None:
            st.warning("Plot no generated (timeout or error)")
        else:
            st.plotly_chart(fig)

    st.markdown("## Assisted Data Processing")
    assistant.set_data(df)
    request = st.text_area("**Describe the data processing desired**", value=DEFAULT_PROMPT_DATA_PROCESSING)
    if st.button("Send Data Processing Request"):
        df_result = assistant.request_process_data(request)
        if df_result is None:
            st.warning("Data Processing no generated (timeout or error)")
        else:
            st.write(df_result)

    if assistant.model == "gpt-3.5-turbo":  # LangChain's Pandas Agent (OpenAI only)
        st.markdown("## Assisted Data Q/A")
        assistant.set_data(df)
        request = st.text_area("**Write your question**", value="")
        if st.button("Send Data Question"):
            result = assistant.request_qa_data(request)
            if result is None:
                st.warning("Answer no generated (timeout or error)")
            else:
                st.markdown(result)

    st.markdown("## Assisted Context Analysis")
    assistant.set_data(df)
    request = st.text_area(
        "**Describe the analysis, explanation or summary desired**", value=DEFAULT_PROMPT_CONTEXT_ANALYSIS
    )
    if st.button("Send Context Analysis Request"):
        result = assistant.request_context_analysis(request)
        if result is None:
            st.warning("Analysis not generated (timeout or error)")
        else:
            st.markdown(result)


def guided_assistant(workflow_context, data_context, input_objects) -> Any:
    """Display the Hybrid Guided Assistant in the UI
    Args:
        df (pd.DataFrame): Dataframe to be used by the assistant
    """

    assistant = st.session_state["assistant"]

    st.markdown("## Assisted Workflow")
    request = st.text_area("**Describe the workflow desired**", value="")
    # remember = "Important: Never create copies of the dataframes, always use inline operations using input_objects"
    # request = f"{request}\n\n{remember}"

    if st.button("Send Improvement Request"):
        result = assistant.request_guided_workflow(
            request,
            workflow_context,
            data_context=data_context,
            input_objects=input_objects,
        )
        if result is None:
            st.warning("Workflow not generated (timeout or error)")
            return None
        return result
    return None


def update_assistant(df: pd.DataFrame = None, data_context=None, topic_context: str = None) -> HybridAssistant:
    """Update the Hybrid Assistant in the UI
    Args:
        df (pd.DataFrame): Dataframe to be used by the assistant
    Returns:
        HybridAssistant: Hybrid Assistant
    """

    assistant = st.session_state["assistant"]

    if df is not None:
        assistant.set_data(df)

    if data_context is not None:
        assistant.set_data_context(data_context)

    if topic_context is not None:
        assistant.set_topic_context(topic_context)

    st.session_state["assistant"] = assistant
    return assistant
