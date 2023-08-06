import numpy as np

def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    Transposes a 2D matrix.

    Args:
        input_matrix (list[list]): The input matrix to be transposed.
    
    Returns:
        list[list]: The transposed matrix.

    Example:
        >>> input_matrix = [[1, 2, 3], [4, 5, 6]]
        >>> transpose2d(input_matrix)
        [[1, 4], [2, 5], [3, 6]]
    """
    num_rows = len(input_matrix)
    num_cols = len(input_matrix[0])

    # Create a new matrix with transposed dimensions
    transposed_matrix = [[0] * num_rows for _ in range(num_cols)]

    # Iterate over the input matrix and assign values to the transposed matrix
    for i in range(num_rows):
        for j in range(num_cols):
            transposed_matrix[j][i] = input_matrix[i][j]

    return transposed_matrix        
    

def window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]:    
    """
    Splits a 1D array into windows of a specified size with a given shift and stride.

    Args:
        input_array (list or np.ndarray): The input 1D array.
        size (int): The size of each window.
        shift (int, optional): The shift between adjacent windows. Defaults to 1.
        stride (int, optional): The stride within each window. Defaults to 1.

    Returns:
        list of lists or list of np.ndarray: The windows.

    Example:
        >>> input_array = [1, 2, 3, 4, 5, 6]
        >>> window1d(input_array, size=3, shift=2, stride=1)
        [[1, 2, 3], [3, 4, 5], [5, 6]]
    """
    if isinstance(input_array, np.ndarray):
        input_array = input_array.tolist()

    num_windows = (len(input_array) - size + shift - 1) // shift + 1
    windows = []

    for i in range(num_windows):
        start = i * shift
        end = start + size
        window = input_array[start:end:stride]
        windows.append(window)

    if isinstance(input_array, np.ndarray):
        windows = [np.array(window) for window in windows]

    return windows


def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride : int = 1) -> np.ndarray:
    """
    Performs 2D convolution on an input matrix using a kernel.

    Args:
        input_matrix (np.ndarray): The input 2D matrix.
        kernel (np.ndarray): The convolution kernel.
        stride (int, optional): The stride for the convolution. Defaults to 1.

    Returns:
        np.ndarray: The convolved matrix.

    Example:
        >>> input_matrix = np.array([[1, 2, 3], [4, 5, 6]])
        >>> kernel = np.array([[0, 1], [1, 0]])
        >>> convolution2d(input_matrix, kernel)
        array([[ 5.,  3.],
               [12.,  6.]])
    """
    # Get dimensions of input matrix and kernel
    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape

    # Calculate output dimensions
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1

    # Initialize output matrix
    output_matrix = np.zeros((output_height, output_width))

    # Perform convolution
    for i in range(output_height):
        for j in range(output_width):
            # Calculate the indices for the current window
            start_row = i * stride
            start_col = j * stride
            end_row = start_row + kernel_height
            end_col = start_col + kernel_width

            # Extract the window from the input matrix
            window = input_matrix[start_row:end_row, start_col:end_col]

            # Perform element-wise multiplication and sum
            output_matrix[i, j] = np.sum(window * kernel)

    return output_matrix
