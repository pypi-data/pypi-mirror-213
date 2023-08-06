# Transformer Lite

Transformer Lite is a Python library that provides lightweight implementations of common matrix transformation operations. It includes functions for transposing a 2D matrix, generating windows from a 1D array, and performing 2D convolution using a kernel.

## Installation

You can install Transformer Lite using pip:

```
pip install transformer-lite
```

## Usage

### transpose2d

This function transposes a 2D matrix, swapping its rows and columns.

```python
from transformer_lite import transpose2d

input_matrix = [[1, 2, 3], [4, 5, 6]]
transposed_matrix = transpose2d(input_matrix)
print(transposed_matrix)
Output:

[[1, 4], [2, 5], [3, 6]]
```

### window1d

The window1d function generates windows from a 1D array with a specified size, shift, and stride.

```python
import numpy as np
from transformer_lite import window1d

input_array = np.array([1, 2, 3, 4, 5, 6])
windows = window1d(input_array, size=3, shift=2, stride=1)
print(windows)
Output:


[array([1, 2, 3]), array([3, 4, 5]), array([5, 6])]
```


### convolution2d

The convolution2d function performs 2D convolution on an input matrix using a kernel.

```python
import numpy as np
from transformer_lite import convolution2d

input_matrix = np.array([[1, 2, 3], [4, 5, 6]])
kernel = np.array([[0, 1], [1, 0]])
convolved_matrix = convolution2d(input_matrix, kernel)
print(convolved_matrix)
Output:

array([[ 5.,  3.],
       [12.,  6.]])
```

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository.
