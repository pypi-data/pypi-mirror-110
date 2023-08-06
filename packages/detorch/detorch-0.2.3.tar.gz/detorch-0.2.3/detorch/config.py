from typing import Optional, Type, Callable, Any, Union, Tuple

import torch
from pipcs import Config, Required, required, Choices

from .de import Policy, DE, Strategy


default_config = Config()


@default_config('environment')
class EnvironmentConfig():
    """**name: environment**

    :ivar Callable[[Any], gym.Env] id: Function that returns a gym environment
    """
    make_env: Required[Callable[[Any], 'gym.Env']] = required


@default_config('policy')
class PolicyConfig():
    """**name: policy**

    :ivar Required[Type[Policy]] policy: torch.nn.Module with a rollout method
    """
    policy: Required[Type[Policy]] = required


@default_config('de')
class DEConfig():
    """**name: de**

    :ivar int population_size
    :ivar int n_step: Number of training steps
    :ivar int n_rollout: Number of episodes per sampled policy.
    :ivar Union[Tuple[float, float], float] differential_weight: The mutation constant.
    :ivar float crossover_probability
    :ivar Strategy strategy: Recombination strategy
    :ivar Optional[int] seed: Random seed
    """
    n_step: Required[int] = required
    n_rollout: int = 1
    population_size: int = 32
    differential_weight: Union[Tuple[float, float], float] = 0.02
    crossover_probability: float = None
    strategy: Choices[Strategy] = Choices(list(Strategy), default=Strategy.best1bin)
    seed: Required[int] = 123
