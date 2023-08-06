from setuptools import setup, find_packages

setup(
    name="validate_models",
    version="0.0.1",
    description="Tools and Instructions for Validation of Classical Models",
    url="http://github.com/Alexandre-Papandrea/validate_models",
    author="Alexandre Papandrea",
    author_email="alexandre@dadosinteligentes.com",
    packages=find_packages(),
    install_requires=[
        "ipywidgets",
        "pandas",
        "numpy",
        "plotly",
        "scikit-learn",
        "scipy",
        "statsmodels",
        "matplotlib",
        "seaborn",
        "ipython"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)