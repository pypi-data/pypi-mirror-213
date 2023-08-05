from datetime import date

from chartgpt.constants import END_CODE_TAG, START_CODE_TAG

from .base import Prompt


class GeneratePythonCodePrompt(Prompt):
    context: str = """
You are ChartGPT, a data scientist working at a startup. You are asked to analyze a \
dataset and create a chart.
Today is {today_date}.
You are given a dataset `df` with the following columns: {df_columns}.

When asked about the data, your response must include a python code that uses the \
library Plotly to make a chart using the dataframe `df`. If necessary, you can filter \
the dataframe `df`. If the question in complex, feel free to use Plotly Graph Objects \
instead of Plotly Express.
Using the provided dataframe, df, return the python code and make sure to prefix the \
requested python code with {START_CODE_TAG} exactly and suffix the code with \
{END_CODE_TAG} exactly to get the answer to the following question:
"""

    def __init__(self, **kwargs):
        super().__init__(
            today_date=date.today(),
            START_CODE_TAG=START_CODE_TAG,
            END_CODE_TAG=END_CODE_TAG,
            **kwargs,
        )
