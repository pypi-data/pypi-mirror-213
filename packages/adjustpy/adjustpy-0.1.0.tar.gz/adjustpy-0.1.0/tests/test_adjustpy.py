import numpy as np
from adjustpy import adjust


def test_missing_method():
    p_values = np.random.random(10)
    try:
        adjust(p_values, method="missing")
        assert False
    except ValueError:
        assert True


def test_bonferroni():
    p_values = np.array([0.02, 0.05, 0.08, 0.11, 0.04])
    p_values_adjusted = adjust(p_values, method="bonferroni")
    assert np.allclose(p_values_adjusted, np.array([0.1, 0.25, 0.4, 0.55, 0.2]))


def test_benjamini_hochberg():
    p_values = np.array([0.02, 0.05, 0.08, 0.11, 0.04])
    p_values_adjusted = adjust(p_values, method="benjamini-hochberg")
    assert np.allclose(
        p_values_adjusted, np.array([0.0833333, 0.08333333, 0.1, 0.11, 0.08333333])
    )


def test_benjamini_yekutieli():
    p_values = np.array([0.02, 0.05, 0.08, 0.11, 0.04])
    p_values_adjusted = adjust(p_values, method="benjamini-yekutieli")
    assert np.allclose(
        p_values_adjusted,
        np.array([0.1902778, 0.1902778, 0.2283333, 0.2511667, 0.1902778]),
    )


def test_benjamini_hochberg_short():
    p_values = np.array([0.02, 0.05, 0.08, 0.11, 0.04])
    p_values_adjusted = adjust(p_values, method="bh")
    assert np.allclose(
        p_values_adjusted, np.array([0.0833333, 0.08333333, 0.1, 0.11, 0.08333333])
    )


def test_benjamini_yekutieli_short():
    p_values = np.array([0.02, 0.05, 0.08, 0.11, 0.04])
    p_values_adjusted = adjust(p_values, method="by")
    assert np.allclose(
        p_values_adjusted,
        np.array([0.1902778, 0.1902778, 0.2283333, 0.2511667, 0.1902778]),
    )


def test_2d():
    p_values = np.random.random((5, 10))
    p_values_adjusted = adjust(p_values, method="bonferroni")
    assert p_values_adjusted.shape == (50,)


def test_3d():
    p_values = np.random.random((5, 10, 10))
    p_values_adjusted = adjust(p_values, method="bonferroni")
    assert p_values_adjusted.shape == (500,)


def test_4d():
    p_values = np.random.random((5, 10, 10, 5))
    p_values_adjusted = adjust(p_values, method="bonferroni")
    assert p_values_adjusted.shape == (2500,)
