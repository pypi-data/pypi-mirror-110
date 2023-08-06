import stribor as st
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchdiffeq import odeint_adjoint, odeint

__all__ = ['ContinuousNormalizingFlow']

# Code adapted from https://github.com/rtqichen/ffjord

class ODEfunc(nn.Module):
    """
    ODE function used in continuous normalizing flows.
    "FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models"
    (https://arxiv.org/abs/1810.01367)

    Args:
        diffeq (Type[nn.Module]): Given inputs `x` and `t`, returns `dx` (and optionally trace)
        divergence (str): How to calculate divergence.
            Options: 'compute', 'compute_set', 'approximate', 'exact'
        rademacher (bool, optional): Whether to use Rademacher distribution for stochastic
            estimator, otherwise uses normal distribution. Default: False
        has_latent (bool, optional): Whether we have latent inputs. Default: False
        set_data (bool, optional): Whether we have set data with shape (..., N, dim). Default: False
    """
    def __init__(self, diffeq, divergence=None, rademacher=False, has_latent=False, set_data=False, **kwargs):
        super().__init__()
        assert divergence in ['compute', 'compute_set', 'approximate', 'exact']

        self.diffeq = diffeq
        self.rademacher = rademacher
        self.divergence = divergence
        self.has_latent = has_latent
        self.set_data = set_data

        self.register_buffer('_num_evals', torch.tensor(0.))

    def before_odeint(self, e=None):
        self._e = e
        self._num_evals.fill_(0)

    def num_evals(self):
        return self._num_evals.item()

    def forward(self, t, states):
        self._num_evals += 1

        y = states[0]
        t = torch.Tensor([t]).to(y)

        latent = mask = None
        if len(states) == 4:
            latent = states[2]
            mask = states[3]
        elif len(states) == 3:
            if self.has_latent:
                latent = states[2]
            else:
                mask = states[2]

        # Sample and fix the noise
        if self._e is None and self.divergence == 'approximate':
            if self.rademacher:
                self._e = torch.randint(low=0, high=2, size=y.shape).to(y) * 2 - 1
            else:
                self._e = torch.randn_like(y)

        if self.divergence == 'exact':
            dy, divergence = self.diffeq(t, y, latent=latent, mask=mask)
        else:
            with torch.set_grad_enabled(True):
                y.requires_grad_(True)
                dy = self.diffeq(t, y, latent=latent, mask=mask)
                if not self.training or 'compute' in self.divergence:
                    if self.set_data or self.divergence == 'compute_set':
                        divergence = st.util.divergence_exact_for_sets(dy, y)
                    else:
                        divergence = st.util.divergence_exact(dy, y)
                else:
                    divergence = st.util.divergence_approx(dy, y, self._e)

        return (dy, -divergence) + tuple(torch.zeros_like(x) for x in states[2:])


class ContinuousNormalizingFlow(nn.Module):
    """
    Continuous normalizing flow.
    "Neural Ordinary Differential Equations" (https://arxiv.org/abs/1806.07366)

    Example:
    >>> torch.manual_seed(123)
    >>> dim = 2
    >>> f = stribor.ContinuousNormalizingFlow(dim, net=stribor.net.DiffeqMLP(dim + 1, [64], dim))
    >>> f(torch.randn(1, dim))
    (tensor([[-0.1527, -0.4164]], tensor([[-0.1218, -0.7133]])

    Args:
        dim (int): Input data dimension
        net (Type[nn.Module]): Neural net that defines a differential equation.
            It takes `x` and `t` and returns `dx` (and optionally trace).
        T (float): Upper bound of integration. Default: 1.0
        divergence: How to calculate divergence. Options:
            `compute`: Brute force approach, scales with O(d^2)
            `compute_set`: Same as compute but for densities over sets with shape (..., N, dim)
            `approximate`: Stochastic estimator, only used during training, O(d)
            `exact`: Exact trace, returned from the `net`
            Default: 'approximate'
        use_adjoint (bool, optional): Whether to use adjoint method for backpropagation,
            which is more memory efficient. Default: True
        solver (string): ODE black-box solver.
            adaptive: `dopri5`, `dopri8`, `bosh3`, `adaptive_heun`
            exact-step: `euler`, `midpoint`, `rk4`, `explicit_adams`, `implicit_adams`
            Default: 'dopri5'
        solver_options (dict, optional): Additional options, e.g. `{'step_size': 10}`. Default: {}
        test_solver (str, optional): Which solver to use during evaluation. If not specified,
            uses the same as during training. Default: None
        test_solver_options (dict, optional): Which solver options to use during evaluation.
            If not specified, uses the same as during training. Default: None
        set_data (bool, optional): If data is of shape (..., N, D). Default: False
        rademacher (bool, optional): Whether to use Rademacher distribution for stochastic
            estimator, otherwise uses normal distribution. Default: False
        atol (float): Absolute tolerance (Default: 1e-5)
        rtol (float): Relative tolerance (Default: 1e-3)
    """
    def __init__(
        self,
        dim,
        net=None,
        T=1.0,
        divergence='approximate',
        use_adjoint=True,
        has_latent=False,
        solver='dopri5',
        solver_options={},
        test_solver=None,
        test_solver_options=None,
        set_data=False,
        rademacher=False,
        atol=1e-5,
        rtol=1e-3,
        **kwargs
    ):
        super().__init__()

        self.T = T
        self.dim = dim

        self.odefunc = ODEfunc(net, divergence, rademacher, has_latent, set_data)

        self.integrate = odeint_adjoint if use_adjoint else odeint

        self.solver = solver
        self.solver_options = solver_options
        self.test_solver = test_solver or solver
        self.test_solver_options = solver_options if test_solver_options is None else test_solver_options

        self.atol = atol
        self.rtol = rtol

    def forward(self, x, latent=None, mask=None, reverse=False, **kwargs):
        # Set inputs
        logp = torch.zeros_like(x)

        # Set integration times
        integration_times = torch.tensor([0.0, self.T]).to(x)
        if reverse:
            integration_times = _flip(integration_times, 0)

        # Refresh the odefunc statistics
        self.odefunc.before_odeint()

        initial = (x, logp)
        if latent is not None:
            initial += (latent,)
        if mask is not None:
            initial += (mask,)

        # Solve ODE
        state_t = self.integrate(
            self.odefunc,
            initial,
            integration_times,
            atol=self.atol,
            rtol=self.rtol,
            method=self.solver if self.training else self.test_solver,
            options=self.solver_options if self.training else self.test_solver_options,
        )

        if len(integration_times) == 2:
            state_t = tuple(s[1] for s in state_t)

        # Collect outputs with correct shape
        x, logp = state_t[:2]
        return x, -logp

    def inverse(self, x, logp=None, latent=None, mask=None, **kwargs):
        return self.forward(x, logp=logp, latent=latent, mask=mask, reverse=True)

    def num_evals(self):
        return self.odefunc._num_evals.item()

def _flip(x, dim):
    indices = [slice(None)] * x.dim()
    indices[dim] = torch.arange(x.size(dim) - 1, -1, -1, dtype=torch.long, device=x.device)
    return x[tuple(indices)]
