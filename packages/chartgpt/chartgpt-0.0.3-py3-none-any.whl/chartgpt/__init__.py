from .chartgpt import ChartGPT


class Chart:
    def __init__(self, df=None, api_key=None, **kwargs):
        self.chartgpt_instance = ChartGPT(api_key=api_key, **kwargs)
        if df is not None:
            self.chartgpt_instance.load(df=df)

    def plot(self, prompt, **kwargs):
        return self.chartgpt_instance.plot(prompt=prompt, **kwargs)

    @property
    def last_run_code(self):
        return self.chartgpt_instance.last_run_code
