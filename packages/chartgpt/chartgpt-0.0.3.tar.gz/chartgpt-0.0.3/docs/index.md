# ChartGPT

ChartGPT is a Python library that leverages the power of GPT to generate Plotly charts from a pandas dataframe with a very simple prompt. Ask it anything, and it will generate a chart for you.

It provides an intuitive and easy-to-use interface for creating visually appealing and interactive charts, making data visualization a breeze.

## Installation

To install ChartGPT, you can use pip:

```bash
pip install chartgpt
```

## Usage

Once installed, you can start using ChartGPT in your Python projects. Here's an example of how to use it:

```Python
from chartgpt import ChartGPT
cg = ChartGPT()
cg.load(df)
cg.plot("State vs. Population")
```

The above code snippet demonstrates the basic usage of ChartGPT. Let's break it down:

1. Import the `ChartGPT` class from the `cg` module.
2. Create an instance of `ChartGPT` using `cg = ChartGPT()`.
3. Load `df` into ChartGPT.
4. Ask ChartGPT to plot the chart with your specific instructions. The model will do the rest 😉

## Additional Resources

- [Plotly Documentation](https://plotly.com/python/)

For detailed usage instructions and advanced features, refer to the official documentation of ChartGPT.

---

ChartGPT is an open-source project maintained by the community. If you have any questions, feedback, or issues, please don't hesitate to reach out on the project's GitHub page. We appreciate your contribution and hope you find ChartGPT useful for your data visualization needs.
