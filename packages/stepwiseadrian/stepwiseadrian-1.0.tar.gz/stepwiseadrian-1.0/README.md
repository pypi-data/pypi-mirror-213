# Stepwise For Model Selection

## License
MIT License
Copyright (c) 2023 Adrian Glazer
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Introduction

Stepwise for Model Selection is a Python package that provides functions for performing model selection using the stepwise regression method. This method is useful for selecting the most significant subset of variables in predicting the target variable. The algorithm is based on the paper by [Kohavi and John (1997)](https://www.sciencedirect.com/science/article/pii/S0020025597000484). The algorithm is implemented in Python.

## Installation

The package can be installed using pip:

```bash pip install AdrianStepwise
```

## Package
The package contains the following functions:
**stepwise()** - Performs stepwise regression on a given dataset and returns the selected variables.

```python  stepwise(df, ci)
```

**Arguments:**
- df: A pandas dataframe containing the dataset.
- ci: The confidence interval for the F-table.
## Usage

The package can be used as follows:

```python import pandas as pd
    import numpy as np
    from AdrianStepwise import stepwise

    # Load data
    data = pd.read_csv('data.csv')
    selection = stepwise(data, ci=0.95)

    # Print results
    print(selection)
```
