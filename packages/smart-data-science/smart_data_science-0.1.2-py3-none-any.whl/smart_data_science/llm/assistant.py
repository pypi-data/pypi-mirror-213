"""
- Title:            LLM-based Assistants.
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress.
"""

# Prompting Principles (https://learn.deeplearning.ai/chatgpt-prompt-eng)

# Principle 1: Write clear and specific instructions
# - Tactic 1: Use delimiters to clearly indicate distinct parts of the input - TODO
# - Tactic 2: Ask for a structured output
# - Tactic 3: Ask the model to check whether conditions are satisfied
# - Tactic 4: Few-shot prompting

# Principle 2: Give the model time to “think”
# - Tactic 1: Specify the steps required to complete a task
# - Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion


from __future__ import annotations

import io
import os
import re
from dataclasses import dataclass
from typing import Any

import langchain
import numpy as np  # noqa   # pylint: disable=unused-import   # needed for LLM code generation (assumes np imported)
import openai
import pandas as pd
import plotly.express as px  # noqa   # pylint: disable=unused-import   # needed for LLM code generation
import vertexai
from dotenv import load_dotenv
from google.cloud import aiplatform

# from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from IPython.display import Markdown, display
from plotly.graph_objects import Figure
from vertexai.preview.language_models import TextGenerationModel

from smart_data_science import logger

log = logger.get_logger(__name__)

USE_PALM_CODE_BISON = True  # If True, the assistant will use the code bison to generate the code

# import Any

MODERATOR = False  # If True, the assistant will check if the user message  complies with OpenAI's usage policies

DEFAULT_TEMPERATURE = 0
TIMEOUT_CODE = 40  # seconds
TIMEOUT_TEXT = 40  # seconds

GLOBAL_DIRECTIVES = {
    "base": "You are a helpful assistant that only focus in solve the user request. ",
    "code_role": "You only return Python code with no comments or further explanations with the format: \
```python <code generated> ``` (markdown). No harmful code nor file modification is allowed. ",
    "markdown_role": "You generate a structured rich-formatted response in Markdown in a \
fancy style (numbers, bold, colors ...). No harmful/hateful commentary or opinion is allowed. ",
}

SPECIFIC_DIRECTIVES = {
    "plot": "The code must generate a plot in plotly and save it in the variable `fig` (do not show it). \
        If the user request is not related to plotting, return a message 'No plot related question.",
    "process_data": "The code generated must process the input data and save the result in the variable `df_result`. \
        In case that the user request is not related to dataframe modification, preparation or processing \
        return a message 'No processing-related question",
    "context_analysis": "The Markdown-generated response must answer the user request with a summary, \
    explanation or analysis based on all the context provided",
    "guided_workflow": "The code generated must follow the workflow instructions provided strictly",
}


def pandas_info_to_string(df: pd.DataFrame) -> str:
    """
    Convert the output of df.info() to a string
    Args:
        df: Dataframe to get the info from
    Returns:
        String with the info
    """
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()


@dataclass
class HybridAssistant:
    """
    Supervised and OpenAI-based assistant. It generates Python code to solve the user request
    """

    df: pd.DataFrame = None  # Dataframe with the data to process, analyze, plot....
    api_key: str = None  # OpenAI API key, if None, it is read from the .env file
    model: str = None  # "gpt-3.5-turbo", "PaLM"
    topic_context: str = None  # Topic context for the LLM model
    data_context: dict | str = None  # Dataframe context
    default_temperature = DEFAULT_TEMPERATURE  # default temperature for the OpenAI model (0= deterministic, 1= random)
    debug: bool = False  # If True, it shows the generated code and the generated text

    def __post_init__(self) -> None:
        """Post initialization"""

        if self.model is None:
            self.model = "gpt-3.5-turbo"

        if self.model == "gpt-3.5-turbo" and self.api_key is None:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key is None:
                raise ValueError("OPENAI_API_KEY not provided nor found in .env file")
            openai.api_key = os.getenv("OPENAI_API_KEY")

        if self.df is not None:
            self.generate_data_context(self.df)

        self.role = {}

        self.role["base"] = GLOBAL_DIRECTIVES["base"]
        self.role["code"] = self.role["base"] + GLOBAL_DIRECTIVES["code_role"]
        self.role["markdown"] = self.role["base"] + GLOBAL_DIRECTIVES["markdown_role"]

        self.role["plot"] = self.role["code"] + SPECIFIC_DIRECTIVES["plot"]
        self.role["process_data"] = self.role["code"] + SPECIFIC_DIRECTIVES["process_data"]
        self.role["context_analysis"] = self.role["markdown"] + SPECIFIC_DIRECTIVES["context_analysis"]
        self.role["guided_workflow"] = self.role["code"] + SPECIFIC_DIRECTIVES["guided_workflow"]

    def set_topic_context(self, text: str) -> None:
        """
        Set the topic context for the OpenAI model
        Args:
            text: Topic context
        """
        self.topic_context = text

    def set_data(self, df: pd.DataFrame) -> None:
        """
        Set the data to process, analyze, plot...
        Args:
            df: Dataframe with the data
        """
        self.df = df
        self.generate_data_context(df)

    def set_data_context(self, custom_context: str | dict) -> None:
        """
        Directly Set the data context for the LLM model
        """
        self.data_context = custom_context

    def generate_data_context(self, df: pd.DataFrame) -> None:
        """
        Automatically Generate the data context for the OpenAI model
        Args:
            df: Dataframe with the data
        Returns:
            Data context
        """
        data_context = {}

        if df is not None:
            data_context["Header"] = df.head(2)
            # data_context["Info"] = pandas_info_to_string(df)
            # data_context["Info"] = df.dtypes.to_dict()
            data_context["Statistics of Numerical Variables"] = (
                df.describe().loc[["mean", "std", "min", "max"]].T.round(3).join(df.dtypes.to_frame("dtype"))
            )

            unique_values = {}
            for column in df.select_dtypes(include=["category"]):
                unique_values[column] = df[column].cat.categories.tolist()
            data_context["Unique Value of Categorical Variables"] = unique_values

            data_context["Description"] = df.describe().loc[["mean", "std", "min", "max"]].round(3)

        self.data_context = data_context

    def generate_request_messages(  # depends on LLM model
        self,
        system_role: str,
        user_request: str,
        workflow_instructions: str,
        topic_context: str,
        data_context: str | dict,
    ) -> list[dict[str, str]] | str:
        """
        Generate the messages to send to the OpenAI model
        Args:
            system_role: System role
            user_request: User request
            workflow_instructions: Specific instructions
            topic_context: Topic context
            data_context: Data context
        Returns:
            List of messages (OpenAI format)
        """
        messages: list[dict[str, str]] | str = ""

        if self.model == "gpt-3.5-turbo":
            if system_role == "langchain_pandas_agent":
                messages = []  # System roles are not sent to the OpenAI model for the pandas agent
            else:
                messages = [{"role": "system", "content": system_role}]

            # messages += [{"role": "user", "content": f"User request (IMPORTANT): {user_request}"}]

            if topic_context:
                messages += [{"role": "user", "content": f"Info about Topic/Problem: ```{topic_context}```"}]

            if data_context:
                messages += [{"role": "user", "content": f"Info about data df: ```{data_context}```"}]

            if workflow_instructions:
                messages += [{"role": "user", "content": f"Workflow instructions: ```{workflow_instructions}```"}]

            # user request
            messages += [
                {
                    "role": "user",
                    "content": f"User request (IMPORTANT GOAL TO FOCUS): \
                          ```{user_request}```",
                }
            ]
            messages += [{"role": "user", "content": system_role}]  # reminder in user request (to avoid losing focus)

        elif self.model == "PaLM":  # Google Gen AI
            messages = f"Your main role: ```{system_role}```\n"

            if topic_context:
                messages += f"Info about Topic/Problem: ```{topic_context}```\n"

            if data_context:
                messages += f"Info about data df: ```{data_context}```\n"

            if workflow_instructions:
                messages += f"Workflow instructions: ```{workflow_instructions}```\n"

            messages += f"Input (User Request): ```{user_request}```\n Output: "

        else:
            log.critical(f"Model {self.model} not supported yet")
            return None

        if self.debug:
            log.info(messages)
            display(messages)
        return messages

    def send_request(
        self,
        messages: list | str,
        type_request: str,
        timeout: int = None,
        moderator: bool = MODERATOR,
        langchain_pandas_agent: bool = False,
        df_langchain_pandas_agent: pd.DataFrame = None,
    ) -> str:
        """
        Send the request to the OpenAI model
        Args:
            messages: List of messages (OpenAI format)
            timeout: Timeout for the request (s)
            moderator: If True, check the message with the moderator endpoint (OpenAI API)
            langchain_pandas_agent: If True, the request is sent to LangChain Pandas Agent (OpenAI API only)
        Returns:
            Response from the OpenAI model
        """
        response: str = None

        if timeout is None:
            timeout = TIMEOUT_TEXT
        log.debug(f"Sending request to {self.model} model with timeout {timeout} s")
        if self.model == "gpt-3.5-turbo":
            # Moderation checkpoint(OpenAI API)
            if moderator:
                try:
                    user_request = str(messages[-1]["content"])  # type: ignore
                    moderator_response = openai.Moderation.create(user_request)  # user request
                    moderator_output = moderator_response["results"][0]
                    if moderator_output["flagged"]:
                        log.critical("Moderation checkpoint triggered")
                        return None
                except openai.error.APIError:
                    log.warning("OpenAI Moderator Endpoint not available")  # The execution continues

            if langchain_pandas_agent:
                agent = langchain.agents.create_pandas_dataframe_agent(
                    langchain.llms.OpenAI(temperature=0, client=None),  # type: ignore
                    df_langchain_pandas_agent,
                    verbose=True,
                    max_execution_time=60,
                )
                response = agent.run(messages)
            else:
                try:
                    full_response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=messages,
                        temperature=self.default_temperature,
                        request_timeout=timeout,
                    )
                    response = full_response.choices[0]["message"]["content"]
                except openai.error.Timeout:
                    log.critical("OpenAI Timeout error")
                    return None
                except openai.error.APIError:
                    log.critical("OpenAI API error")
                    return None
                except openai.error.RateLimitError:
                    log.critical("OpenAI Rate limit error")
                    return None

            # Todo: Include LangChain Pandas Agent - Another basic assistant? (tested OK)

        elif self.model == "PaLM":

            def _predict_large_language_model_sample(
                project_id: str,
                model_name: str,
                temperature: float,
                max_decode_steps: int,
                top_p: float,
                top_k: int,
                content: str,
                location: str = "us-central1",
                tuned_model_name: str = "",
            ):
                """Predict using a Large Language Model."""
                vertexai.init(project=project_id, location=location)
                model = TextGenerationModel.from_pretrained(model_name)
                if tuned_model_name:
                    model = model.get_tuned_model(tuned_model_name)
                full_response = model.predict(
                    content,
                    temperature=temperature,
                    max_output_tokens=max_decode_steps,
                    top_k=top_k,
                    top_p=top_p,
                )
                return full_response.text

            messages = str(messages)

            def _predict_large_language_model_sample_code(
                api_endpoint: str,
                endpoint: str,
                input: str,
                parameters: str,
                location: str = "us-central1",
            ):
                # The AI Platform services require regional API endpoints.
                client_options = {"api_endpoint": api_endpoint}
                # Initialize client that will be used to create and send requests.
                # This client only needs to be created once, and can be reused for multiple requests.
                client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
                instance_dict = input
                instance = json_format.ParseDict(instance_dict, Value())
                instances = [instance]
                parameters_dict = parameters
                parameters = json_format.ParseDict(parameters_dict, Value())
                response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
                return response.predictions[0]["content"]

            if (type_request == "text") or (USE_PALM_CODE_BISON is False):  # in evaluation
                response = _predict_large_language_model_sample(
                    # "spa-ai-solutions-sdb-002", "text-bison@001", 0, 1024, 0.8, 40, messages, "us-central1"
                    "spa-ai-solutions-sdb-002",
                    "text-bison@001",
                    0,
                    1024,
                    0.8,
                    0,
                    messages,
                    "us-central1",  # deterministic
                )
            elif type_request == "code":
                response = _predict_large_language_model_sample_code(
                    "us-central1-aiplatform.googleapis.com",
                    "projects/spa-ai-solutions-sdb-002/locations/us-central1/publishers/google/models/code-bison@001",
                    {"prefix": messages},
                    {"temperature": 0, "maxOutputTokens": 256},
                    "us-central1",
                )

        else:
            log.critical(f"Model {self.model} not supported yet")
            return None

        # post process PaLM response
        # if fig.show() in response, remove it:
        if response is not None:
            if "fig.show()" in response:
                response = response.replace("fig.show()", "")
                log.warning("Removed fig.show() from response")

        return response

    def perform_request(
        self,
        system_role: str,
        user_request: str,
        type_request: str = "text",  # text (includes markdown...) or code to be executed
        workflow_instructions: str = None,  # Here include an example of the request if available (needed for PaLM)
        df: pd.DataFrame = None,
        data_context: str | dict = None,
        topic_context: str = None,
    ) -> str:
        """
        Code assistant based on GPT-3.5-turbo model. It generates Python code to solve the user request.
        Args:
            system_role: Role of the LLM Model
            user_request: User request to solve
            type_request: Type of request: text or code
            workflow_instructions: Specific instructions for the LLM model
            df: Dataframe with the data to process, analyze, plot....
            data_context: Dataframe context
            topic_context: Topic context for the LLM model

        Returns:
            Generated code (Markdown string)
        """
        if df is None:
            df = self.df.copy()
        else:
            log.info("Dataframe provided, saving data and generating data context")
            self.set_data(df)
            self.generate_data_context(df)

        if data_context is None:
            data_context = self.data_context

        if topic_context is None:
            topic_context = self.topic_context

        langchain_pandas_agent = False
        df_langchain_pandas_agent = None
        if system_role == "langchain_pandas_agent":
            langchain_pandas_agent = True
            df_langchain_pandas_agent = df.copy()

        messages = self.generate_request_messages(
            system_role, user_request, workflow_instructions, topic_context, data_context
        )

        # 2 - Send Request to LLM model
        if type_request == "code":
            timeout = TIMEOUT_CODE
        else:
            timeout = TIMEOUT_TEXT

        assistant_text = self.send_request(
            messages,
            type_request=type_request,
            timeout=timeout,
            langchain_pandas_agent=langchain_pandas_agent,
            df_langchain_pandas_agent=df_langchain_pandas_agent,
        )

        # 3 - Parse and execute the code generated
        if assistant_text is None:
            return None

        if type_request == "code" and self.debug:
            log.info("Code Generated:")
            log.info(assistant_text)
            display(Markdown(assistant_text))

        return assistant_text

    def extract_and_execute_assistant_code(
        self, assistant_text: str, df: pd.DataFrame = None, input_objects: dict = None
    ) -> dict[str, Any] | None:
        """
        Extract the code generated by the assistant and execute it
        Args:
            assistant_text: Text generated by the assistant
            df: Dataframe with the data (basic assistant)
            input_objects: Dictionary with the input objects (guided workflow assistant)
        Returns:
            Dictionary with the variables extracted from the code
        """

        # execute assistant-generated code
        if assistant_text is None:
            return None

        if input_objects is not None:
            log.debug("Input objects provided, using guided workflow assistant")
        elif df is None:
            df = self.df.copy()
            log.debug("No input objects provided and No dataframe provided, using basic assistant with default df")

        # display(assistant_text)

        matches = re.findall("```(?:python)?\n(.*)\n```", assistant_text, re.DOTALL)
        local_variables = locals()
        # display(local_variables.keys())
        returned_text = None
        if len(matches) > 0:
            returned_text = matches[0]
            # Execute the Python code and extract the target variables
            try:
                exec(returned_text, globals(), local_variables)  # pylint: disable=exec-used
            except Exception as e:  # pylint: disable=broad-exception-caught
                log.warning(f"Error executing the code: {e}")
            # else:
            #     log.warning("No code block found in the text")
        return local_variables

    def request_plot(
        self,
        user_request: str,
        df: pd.DataFrame = None,
        data_context: str | dict = None,
        topic_context: str = None,
        show_result: bool = False,
    ) -> Figure:
        """
        Plotter assistant based on GPT-3.5-turbo model. It generates Python code to plot the data in the dataframe `df`.
        The code is generated based on the user_request and the context provided.
        The context is the dataframe `df` and the problem context.
        The problem context is the problem description and the data source. The user_request is the user
        request to plot the data.
        Args:
            user_request: User request to plot the data.
            df: Dataframe with the data to plot.
            data_context: Dataframe context.
            topic_context: Topic context for the LLM model.
            show_result: If True, the plot is shown.
        Returns:
            Plotly Figure with the plot
        """

        # 1 - Prepare the request
        system_role = self.role["plot"]
        specific_instructions = """The input dataframe is 'df', the predictions, if exists, are in column 'predicted'.
            Import the required libraries e.g: ``` import plotly.express as px ```. Do not show the figure.

            """
        # Example:
        # input: Generate a 3d graph with prediction vs target and unemployment rate colored by fuel price
        # output:
        # ```python
        # import plotly.express as px
        # # do not use 'target' as column name, use the name of the target column
        # fig = px.scatter_3d(df, x='prediction', y='target', z='unemployment_rate', color='fuel_price')
        # # Do not show the figure
        # ```
        # """

        type_request = "code"

        # 2 - Request the code
        assistant_text = self.perform_request(
            system_role, user_request, type_request, specific_instructions, df, data_context, topic_context
        )
        if assistant_text is None:
            log.warning(f"No code generated: {assistant_text}")
            return None

        # 3 -Parse and execute the code generated
        returned_variables = self.extract_and_execute_assistant_code(assistant_text, df)

        # 4 -Return the plot
        if returned_variables is None:
            log.warning(f"No variables returned: {assistant_text}")
            return None

        fig = returned_variables.get("fig", None)
        if fig is not None:
            log.info("Figure generated and saved in variable `fig`")
            if show_result:
                fig.show()
            return fig

        log.warning(f"No figure generated: {assistant_text}")
        return None

    def request_process_data(
        self,
        user_request: str,
        df: pd.DataFrame = None,
        data_context: str | dict = None,
        topic_context: str = None,
        show_result: bool = False,
    ) -> pd.DataFrame:
        """
        Data Processor assistant based on GPT-3.5-turbo model.
        Args:
            user_request: User request to plot the data.
            data: Dataframe with the data to plot.
            data_context: Dataframe context.
            topic_context: Topic context for the LLM model.
            show_result: If True, the plot is shown.

        Returns:
            Dataframe with the processed data
        """

        # 1 - Prepare the request
        system_role = self.role["process_data"]
        specific_instructions = "The input dataframe is 'df', the predictions, is any goes into the column 'predicted'"
        type_request = "code"

        # 2 - Request the code
        assistant_text = self.perform_request(
            system_role,
            user_request,
            type_request,
            specific_instructions,
            df,
            data_context,
            topic_context,
        )
        if assistant_text is None:
            log.warning(f"No result generated: {assistant_text}")
            return None

        # 3 -Parse and execute the code generated
        returned_variables = self.extract_and_execute_assistant_code(assistant_text, df)

        # else:
        #     log.warning("No code block found in the text")

        if returned_variables is None:
            log.warning(f"No variables returned: {assistant_text}")
            return None

        # 4 -Return the dataframe
        df_result = returned_variables.get("df_result", None)
        if df_result is not None:
            log.info("Result generated and saved in the variable 'df_result'")
            if show_result:
                display(df_result)
            return df_result

        log.warning(f"No Processed Data: {assistant_text}")
        return None

    def request_context_analysis(
        self,
        user_request: str,
        df: pd.DataFrame = None,
        data_context: str | dict = None,
        topic_context: str = None,
    ) -> str:
        """
        Context Analysis assistant based on GPT-3.5-turbo model.
        Args:
            user_request: User request to plot the data.
            data: Dataframe with the data to plot.
            data_context: Dataframe context.
            topic_context: Topic context for the LLM model.
        Returns:
            Text with the context analysis requested
        """

        # 1 - Prepare the request
        system_role = self.role["context_analysis"]
        specific_instructions = "The input dataframe is 'df', the predictions, is any goes into the column 'predicted'"
        type_request = "text"

        # 2 - Perform Request
        assistant_text = self.perform_request(
            system_role, user_request, type_request, specific_instructions, df, data_context, topic_context
        )
        if assistant_text is None:
            log.warning(f"No Response generated: {assistant_text}")
            return None

        return assistant_text

    def request_qa_data(
        self,
        user_request: str,
        df: pd.DataFrame = None,
        data_context: str | dict = None,
        topic_context: str = None,
    ) -> str:
        """
        Data Q/A Assistant based LangcHain's Pandas Agent on GPT-3.5-turbo model.
        Args:
            user_request: User request to plot the data.
            data: Dataframe with the data to plot.
            data_context: Dataframe context.
            topic_context: Topic context for the LLM model.
        Returns:
            Text with the answer generated
        """

        # 1 - Prepare the request
        system_role = "langchain_pandas_agent"  # langchain will use its own role
        specific_instructions = "The input dataframe is 'df', the predictions, is any goes into the column 'predicted'"
        type_request = "text"

        # 2 - Perform Request
        assistant_text = self.perform_request(
            system_role, user_request, type_request, specific_instructions, df, data_context, topic_context
        )
        if assistant_text is None:
            log.warning(f"No Response generated: {assistant_text}")
            return None

        return assistant_text

    def request_guided_workflow(
        self,
        user_request: str,
        workflow_instructions: str,
        data_context: str | dict = None,
        topic_context: str = None,
        input_objects: dict = None,
    ) -> dict:
        """
        Data Processor assistant based on GPT-3.5-turbo model.
        Args:
            user_request: User request to plot the data.
            workflow_instructions: Workflow context.
            data_context: Data (summaries) and context.
            input_objects: Input objects required to execute the workflow.
        Returns:
            Dataframe with the processed data
        """

        # 1 - Prepare the request
        system_role = self.role["guided_workflow"]
        type_request = "code"

        # 2 - Request the code
        assistant_text = self.perform_request(
            system_role=system_role,
            user_request=user_request,
            type_request=type_request,
            workflow_instructions=workflow_instructions,
            data_context=data_context,
            topic_context=topic_context,
        )
        if assistant_text is None:
            log.warning(f"No result generated: {assistant_text}")
            return None

        # 3 -Parse and execute the code generated
        returned_variables = self.extract_and_execute_assistant_code(assistant_text, input_objects=input_objects)

        # else:
        #     log.warning("No code block found in the text")

        # 4 -Return the result
        # df_result = returned_variables.get("df_result", None)
        # if df_result is not None:
        #     log.info("Result generated and saved in the variable 'df_result'")
        #     if debug:
        #         log.debug("Result:")
        #         display(df_result)
        #     return df_result
        if returned_variables is not None:
            log.debug("Result generated and saved in the variable 'returned_variables'")
            # if debug:
            #     log.debug("Result:")
            #     display(returned_variables)
            return returned_variables

        log.warning(f"No Processed Data: {assistant_text}")
        return None


# Request with LangChain. Tested: Similar results obtained. Not needed for now

# from langchain.llms import OpenAI
# llm = OpenAI(temperature=0, max_execution_time=60))
# response = (message)
# Markdown(response)

# TODO (Optional) Request with Langchain's Pandas Agent. TESTED: Can be useful as another hybrid agent
# from langchain.llms import OpenAI
# from langchain.agents import create_pandas_dataframe_agent
# agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True, max_execution_time=60))
# result = agent.run("Description about the data you are working with", max_execution_time=60)
# result = agent.run("Top anomaly samples (larger deviation between prediction and target)")
# result = agent.run("Top anomaly samples (larger deviation between prediction and target) and the contribution
# of each feature to the prediction")


# def request_process(request, df=None, data_context=None, problem_context=None, show_output=True):
#     df = df.copy()

#     system_role = "You are a helpful assistant that only returns Python code with no comments or explanations \
#         that solves the user request. The input dataframe is 'df', the prediction, \
#         if any, goes into the column 'predicted'. Always save the processed dataframe in 'df_result' (do not show it)\
#         . No harmful code nor file modification is allowed \
#         If the request is not related to data processing, return a message 'No Data Processing question"

#     if data_context is None and df is not None:
#         data_context = f"Header of df': {df.head(5)}"  #  default context
#         # display(data_context["df"])
#     messages = [{"role": "system", "content": system_role}]

#     if data_context is not None:
#         messages += [{"role": "user", "content": f"Info about data df: {data_context}"}]
#     if problem_context is not None:
#         messages += [{"role": "user", "content": f"Info about problem: {problem_context}"}]

#     messages += [{"role": "user", "content": f"Request: {request}"}]

#     # display(messages)

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         temperature=0.05,
#     )
#     text = response.choices[0]["message"]["content"]

#     log.info("Code Generated:")
#     display(Markdown(text))

#     matches = re.findall("```(?:python)?\n(.*)\n```", text, re.DOTALL)

#     loc = locals()

#     if len(matches) > 0:
#         python_code = matches[0]
#         # Execute the Python code and extract the target variables
#         exec(python_code, globals(), loc)
#     else:
#         log.info("No code block found in the text")

#     if "df_result" in loc:
#         log.info("result generated and saved in the variable `df_result`")
#         if show_output:
#           display(loc.get("df_result", None))
#     return loc
