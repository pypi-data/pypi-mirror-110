import torch
import torch.distributions as td

class Uniform(td.Independent):
    """
    Uniform distribution.

    Example:
    >>> dist = stribor.Uniform(0., 1.)
    >>> dist.log_prob(torch.zeros(1, 2))
    tensor([[0., 0.]])
    >>> dist = stribor.Uniform(torch.zeros(2), torch.ones(2))
    >>> dist.log_prob(torch.zeros(1, 2))
    tensor([0.])

    Args:
        low (float or tensor): Low bound (inclusive)
        high (float or tensor): High bound (exclusive)
    """
    def __init__(self, low, high, reinterpreted_batch_ndims=1, **kwargs):
        self.low = low
        self.high = high

        rbd = 0 if isinstance(self.low, float) else 1

        super().__init__(td.Uniform(self.low, self.high, **kwargs), reinterpreted_batch_ndims=rbd)

class UnitUniform(Uniform):
    """
    Unit uniform distribution.

    Example:
    >>> dist = stribor.UnitUniform(2)
    >>> dist.log_prob(torch.zeros(1, 2))
    tensor([0.])

    Args:
        dim (int): Dimension of data
    """
    def __init__(self, dim):
        self.dim = dim
        super().__init__(torch.zeros(self.dim), torch.ones(self.dim))
