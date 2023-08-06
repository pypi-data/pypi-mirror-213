![Gauge Logo](./logo.png)

# Gauge - LLM Evaluation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/gauge-llm.svg)](https://pypi.org/project/gauge-llm/)

Gauge is a Python library for evaluating and comparing language models (LLMs). Compare models based on their performance on complex and custom tasks, alongside numeric measurements like latency and cost.

## How does it work?

Gauge uses a model-on-model approach to evaluate LLMs qualitatively. An advanced arbiter model (GPT-4) evaluates the performance of smaller LLMs on specific tasks, providing a numeric score based on their output. This allows users to create custom benchmarks for their tasks and obtain qualitative evaluations of different LLMs. Gauge is useful for evaluating and ranking LLMs on a wide range of complex and subjective tasks, such as creative writing, staying in character, formatting outputs, extracting information, and translating text.

## Features

- Evaluate and compare multiple LLMs using custom benchmarks
- Straightforward API for running and evaluating LLMs
- Extensible architecture for including additional models

## Installation

To install Gauge, run the following command:

```bash
pip install gauge-llm
```

Before using Gauge, set your HUGGINGFACE_TOKEN environment variable, your REPLICATE_API_TOKEN, and import the `openai` library and set your `.api_key`.

```python
import os
import openai

os.environ["HUGGINGFACE_TOKEN"] = "your_huggingface_token"
os.environ["REPLICATE_API_TOKEN"] = "your_replicate_api_token"
openai.api_key = "your_openai_api_key"
```

## Examples

### Information Extraction: Historical Event

```python
import gauge

query = "Extract the main points from the following paragraph: On July 20, 1969, American astronauts Neil Armstrong and Buzz Aldrin became the first humans to land on the Moon. Armstrong stepped onto the lunar surface and described the event as 'one small step for man, one giant leap for mankind.'"
gauge.evaluate(query)
```

### Staying in Character: Detective's Monologue

```python
import gauge

query = "Write a monologue for a detective character in a film noir setting."
gauge.evaluate(query)
```

### Translation: English to Spanish

```python
import gauge

query = "Translate the following English text to Spanish: 'The quick brown fox jumps over the lazy dog.'"
gauge.evaluate(query)
```

### Formatting Output: Recipe Conversion

```python
import gauge

query = "Convert the following recipe into a shopping list: 2 cups flour, 1 cup sugar, 3 eggs, 1/2 cup milk, 1/4 cup butter."
gauge.evaluate(query)
```

These examples will display a table with the results for each model, including their name, response, score, explanation, latency, and cost.

## API

### `gauge.run(model, query)`

Runs the specified model with the given query and returns the output, latency, and cost.

**Parameters:**

- `model`: A dictionary containing the model's information (type, name, id, and price_per_second).
- `query`: The input query for the model.

**Returns:**

- `output`: The generated output from the model.
- `latency`: The time taken to run the model.
- `cost`: The cost of running the model.

### `gauge.evaluate(query)`

Evaluates multiple LLMs using the given query and displays a table with the results, including the model's name, response, score, explanation, latency, and cost.

**Parameters:**

- `query`: The input query for the models.

## Contributing

Contributions to Gauge are welcome! If you'd like to add a new model or improve the existing code, please submit a pull request. If you encounter issues or have suggestions, open an issue on GitHub.

## License

Gauge is released under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgements

This project was created by Killian Lucas and Roger Hu during the AI Tinkerers Summer Hackathon, which took place on June 10th, 2023 in Seattle at Create 33. The event was sponsored by AWS Startups, Cohere, Madrona Venture Group, and supported by Pinecone, Weaviate, and Blueprint AI. Gauge made it to the semi-finals.