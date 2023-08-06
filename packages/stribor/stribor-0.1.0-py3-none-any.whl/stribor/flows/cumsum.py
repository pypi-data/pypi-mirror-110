import torch
import torch.nn as nn
import torch.nn.functional as F


def diff(x, dim=-1):
    """
    Inverse of x.cumsum(dim=dim).
    Compute differences between subsequent elements of the tensor.
    Only works on dims -1 and -2.

    Args:
        x (tensor): Input of arbitrary shape
    Returns:
        diff (tensor): Result with the same shape as x
    """
    if dim == 1:
        if x.dim() == 2:
            dim = -1
        elif x.dim() == 3:
            dim = -2
        else:
            raise ValueError('If dim=1, tensor must have 2 or 3 dimensions')

    if dim == 2:
        if x.dim() == 3:
            dim = -1
        elif x.dim() == 4:
            dim = -2
        else:
            raise ValueError('If dim=2, tensor should have 3 or 4 dimensions')

    if dim == -1:
        return x - F.pad(x, (1, 0))[..., :-1]
    elif dim == -2:
        return x - F.pad(x, (0, 0, 1, 0))[..., :-1, :]
    else:
        raise ValueError("dim must be equal to -1 or -2")


class Cumsum(nn.Module):
    """
    Compute cumulative sum along the specified dimension of the tensor.

    Example:
    >>> f = stribor.Cumsum(-1)
    >>> f(torch.ones(1, 4))
    (tensor([[1., 2., 3., 4.]]), tensor([[0., 0., 0., 0.]]))

    Args:
        dim (int): Tensor dimension over which to perform the summation. Options: -1 or -2.
    """
    def __init__(self, dim):
        super().__init__()
        assert dim in [-1, -2], '`dim` must be either `-1` or `-2`'
        self.dim = dim

    def forward(self, x, **kwargs):
        y = x.cumsum(self.dim)
        return y, torch.zeros_like(y)

    def inverse(self, y, **kwargs):
        x = diff(y, self.dim)
        return x, torch.zeros_like(x)

class Diff(nn.Module):
    """
    Inverse of Cumsum transformation.

    Args:
        dim (int): Tensor dimension over which to perform the diff. Options: -1 or -2.
    """
    def __init__(self, dim):
        super().__init__()
        self.base_flow = Cumsum(dim)

    def forward(self, x, **kwargs):
        return self.base_flow.inverse(x, **kwargs)

    def inverse(self, x, **kwargs):
        return self.base_flow.forward(x, **kwargs)


class CumsumColumn(nn.Module):
    """
    Cumulative sum along the specific column in (..., M, N) matrix.

    Example:
    >>> f = stribor.CumsumColumn(1)
    >>> f(torch.ones(3, 3))[0]
    tensor([[1., 1., 1.],
            [1., 2., 1.],
            [1., 3., 1.]])

    Args:
        column (int): Column in the (batched) matrix (..., M, N) over which to
            perform the summation
    """
    def __init__(self, column):
        super().__init__()
        self.column = column

    def forward(self, x, **kwargs):
        y = x.clone()
        y[..., self.column] = y[..., self.column].cumsum(-1)
        return y, torch.zeros_like(y)

    def inverse(self, y, **kwargs):
        x = y.clone()
        x[..., self.column] = diff(x[..., self.column], -1)
        return x, torch.zeros_like(x)

class DiffColumn(nn.Module):
    def __init__(self, column):
        super().__init__()
        self.base_flow = CumsumColumn(column)

    def forward(self, x, **kwargs):
        return self.base_flow.inverse(x, **kwargs)

    def inverse(self, x, **kwargs):
        return self.base_flow.forward(x, **kwargs)
