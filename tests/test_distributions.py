import numpy as np
import pytest

from ensemble.distributions import (
    Beta,
    Exponential,
    Fisk,
    Gamma,
    GumbelR,
    InvGamma,
    LogNormal,
    Normal,
    Weibull,
)

NEG_MEAN = -2
BETA_MEAN = 0.5
BETA_VARIANCE = 0.2
MEAN = 4
VARIANCE = 2


def test_exp():
    assert Exponential.support == (0, np.inf)
    # assert Exponential._support == (0, np.inf)
    exp = Exponential(MEAN, VARIANCE)
    assert exp.support == (0, np.inf)
    res = exp.stats(moments="mv")
    exp_var = MEAN**2
    assert np.isclose(res[0], MEAN)
    assert np.isclose(res[1], exp_var)


def test_gamma():
    gamma = Gamma(MEAN, VARIANCE)
    res = gamma.stats(moments="mv")
    assert np.isclose(res[0], MEAN)
    assert np.isclose(res[1], VARIANCE)


def test_invgamma():
    invgamma = InvGamma(MEAN, VARIANCE)
    res = invgamma.stats(moments="mv")
    assert np.isclose(res[0], MEAN)
    assert np.isclose(res[1], VARIANCE)


# TODO: WRITE ADDITIONAL TESTS DUE TO NUMERICAL SOLUTION, CURRENTLY UNDERPERFORMING WITH MEAN = [1, 3]
def test_fisk():
    fisk = Fisk(MEAN, VARIANCE)
    res = fisk.stats(moments="mv")
    assert np.isclose(res[0], MEAN)
    assert np.isclose(res[1], VARIANCE)


def test_gumbel():
    gumbel = GumbelR(MEAN, VARIANCE)
    res = gumbel.stats(moments="mv")
    assert np.isclose(res[0], MEAN)
    assert np.isclose(res[1], VARIANCE)

    gumbel = GumbelR(NEG_MEAN, VARIANCE)
    res = gumbel.stats(moments="mv")
    assert np.isclose(res[0], NEG_MEAN)
    assert np.isclose(res[1], VARIANCE)


def test_weibull():
    weibull = Weibull(624.25, 183.791**2)
    res = weibull.stats(moments="mv")
    print("resulting mean and var: ", res)
    assert np.isclose(res[0], MEAN)
    assert np.isclose(res[1], VARIANCE)


def test_lognormal():
    lognormal = LogNormal(MEAN, VARIANCE)
    res = lognormal.stats(moments="mv")
    print("resulting mean and var: ", res)
    assert np.isclose(res[0], MEAN)
    assert np.isclose(res[1], VARIANCE)


def test_normal():
    norm = Normal(MEAN, VARIANCE)
    res = norm.stats(moments="mv")
    assert np.isclose(res[0], MEAN)
    assert np.isclose(res[1], VARIANCE)

    norm = Normal(NEG_MEAN, VARIANCE)
    res = norm.stats(moments="mv")
    assert np.isclose(res[0], NEG_MEAN)
    assert np.isclose(res[1], VARIANCE)


def test_beta():
    beta = Beta(BETA_MEAN, BETA_VARIANCE)
    # beta = Beta(0.5, 0.249)
    res = beta.stats(moments="mv")
    assert np.isclose(res[0], BETA_MEAN)
    assert np.isclose(res[1], BETA_VARIANCE)


def test_invalid_means():
    # negative means for only positive RVs
    with pytest.raises(ValueError):
        Exponential(NEG_MEAN, VARIANCE)
    with pytest.raises(ValueError):
        Gamma(NEG_MEAN, VARIANCE)
    with pytest.raises(ValueError):
        InvGamma(NEG_MEAN, VARIANCE)
    with pytest.raises(ValueError):
        Fisk(NEG_MEAN, VARIANCE)

    # mean outside of 0 and 1 for Beta
    with pytest.raises(ValueError):
        Beta(NEG_MEAN, VARIANCE)


def test_invalid_custom_supports():
    with pytest.raises(ValueError):
        Exponential(1, 1, ub=2)
    with pytest.raises(ValueError):
        Exponential(1, 1, lb=-np.inf)
    with pytest.raises(ValueError):
        Exponential(1, 1, ub=np.inf)
    with pytest.raises(ValueError):
        Normal(1, 1, lb=0)
    with pytest.raises(ValueError):
        Normal(1, 1, ub=0)
