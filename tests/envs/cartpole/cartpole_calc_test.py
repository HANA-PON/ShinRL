import chex
import numpy.testing as npt
import pytest

from shinrl import CartPole


@pytest.fixture
def setUp():
    config = CartPole.DefaultConfig(dA=5)
    return config


def test_to_discrete_act(setUp):
    from shinrl.envs.mountaincar.calc import to_discrete_act

    config = setUp
    act = to_discrete_act(config, -0.4)

    # jit testing
    config10 = CartPole.DefaultConfig(dA=50)
    act = to_discrete_act(config10, -0.4)


def test_to_continuous_act(setUp):
    from shinrl.envs.mountaincar.calc import to_continuous_act

    config = setUp
    act = to_continuous_act(config, 2)


def test_state_to_x_th(setUp):
    from shinrl.envs.cartpole.calc import state_to_x_th

    config = setUp
    _ = state_to_x_th(config, 1)


def test_x_th_to_state(setUp):
    from shinrl.envs.cartpole.calc import x_th_to_state

    config = setUp
    _ = x_th_to_state(config, -1.0, -1.0, 0.0, 0.0)


def test_transition(setUp):
    from shinrl.envs.cartpole.calc import transition

    config = setUp
    next_state, probs = transition(config, 1, 2)
    chex.assert_shape(next_state, (1,))
    chex.assert_shape(probs, (1,))


def test_reward(setUp):
    from shinrl.envs.cartpole.calc import reward

    config = setUp
    rew = reward(config, 1, 2)


def test_observation():
    from shinrl.envs.cartpole.calc import observation_tuple

    config = CartPole.DefaultConfig()
    obs = observation_tuple(config, 1)
    chex.assert_shape(obs, (4,))
