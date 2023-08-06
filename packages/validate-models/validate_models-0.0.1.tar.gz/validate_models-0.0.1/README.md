Sure, here is the translated version of your provided text:

# Validate Models

![Python versions](https://img.shields.io/pypi/pyversions/validate_models)
[![GitHub Issues](https://img.shields.io/github/issues/Alexandre-Papandrea/validate_models)](https://github.com/Alexandre-Papandrea/validate_models/issues)
[![License](https://img.shields.io/github/license/Alexandre-Papandrea/validate_models)](https://github.com/Alexandre-Papandrea/validate_models/blob/main/LICENSE)

`validate_models` is a Python library designed to make the validation of Machine Learning models more accessible and efficient. With a comprehensive set of graphs and metrics, this library helps to simplify and accelerate the validation stage of the Machine Learning pipeline.

## 🛠️ Installation

You can install the `validate_models` library via pip:

```shell
pip install validate_models
```

## 🚀 Usage

First, import the function `validate_regression` or `validate_binary_classification` from `validate_models`:

```python
from validate_models import validate_regression
from validate_models import validate_binary_classification
```

Then, call the function `validate_regression` or `validate_binary_classification` passing the appropriate arguments. For example:

```python
validate_regression(model, X_train, y_train, X_test, y_test, cv)
validate_binary_classification(model, X_train, y_train, X_test, y_test, cv, nbins, n_repeats)
```

## 🧪 Tests

To run the tests, use the following command:

```shell
pytest
```

## 🤝 Contribution

We welcome all contributions, whether fixing bugs, adding new features, or improving documentation. Here are some guidelines:

1. Fork the repository and create a new branch.
2. Make your changes in the new branch.
3. Run the tests to ensure your changes do not break anything.
4. Make a pull request describing your changes.

If you have any questions or suggestions, feel free to open an issue.

## 👥 Maintainers

- [Alexandre Papandrea](https://github.com/Alexandre-Papandrea)

## 📜 License

`validate_models` is licensed under the terms of the [MIT License](LICENSE).

Read the full post about `validate_models` on [Medium](https://medium.com/@Alexandre-Papandrea/validating-machine-learning-models-with-python-library-validate_models-2fe64a6d1ae5).
