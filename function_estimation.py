"""
A/B Testing Backend Logic

This module implements the core mathematical and plotting functionalities for A/B testing. 
It includes:
1. Calculation of sample size and test duration.
2. Estimation of Minimum Detectable Effect (MDE).
3. Visualization of hypothesis testing through power analysis plots.


"""

from math import sqrt
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from src.a_btest.API.APIModels import *


def get_sz_duration(duration_parameter: DurationParameter) -> tuple[float, int]:
    if duration_parameter.metric_type == "binomial":
        duration_parameter.baseline_metric = duration_parameter.baseline_metric / 100
        sigma_2 = duration_parameter.baseline_metric * (1 - duration_parameter.baseline_metric)

    else:
        sigma_2 = duration_parameter.std**2
    c = 100 / duration_parameter.control_allocation + 100 / duration_parameter.variant_allocations
    if duration_parameter.hypothesis == "One-sided Test":
        # fmt: off
        m = (c* sigma_2* ((norm.ppf(1 - duration_parameter.significance_level*0.01/ duration_parameter.number_of_variants) + norm.ppf(1 - duration_parameter.beta*0.01)) ** 2) / (0.01*duration_parameter.baseline_metric * duration_parameter.min_detectable_effect_percentage) ** 2)
    else:
        m = (c * sigma_2 * (norm.ppf(1 - duration_parameter.significance_level / duration_parameter.number_of_variants) + norm.ppf(1 - duration_parameter.beta * 0.01)) ** 2) / (
            duration_parameter.baseline_metric * duration_parameter.min_detectable_effect_percentage * 0.01
        ) ** 2
    if duration_parameter.daily_visitors == 0:
        # raise ValueError("Daily traffic should be greater than 0")
        return 0
    duration = round(m / duration_parameter.daily_visitors) + 1
    return (round(m), duration)
    # fmt: on


def calculate_mde(mde_parameter: Mde_Parameter) -> float:
    z_alpha = norm.ppf(1 - mde_parameter.significance_level * 0.01 / mde_parameter.number_of_variants)
    z_beta = norm.ppf(mde_parameter.beta * 0.01)
    baseline = mde_parameter.weekly_conversions / mde_parameter.weekly_visitors
    mde = 2 * (z_alpha - z_beta) * sqrt((mde_parameter.number_of_variants) * baseline * (1 - baseline) / (mde_parameter.weekly_visitors * baseline**2))
    return mde


def generate_plot(obj: VisualParameter) -> plt:
    # Calculate standard deviation (sigma) based on baseline conversion rate
    sigma = 0.01 * np.sqrt(obj.baseline_conversion_rate_percentage * (100 - obj.baseline_conversion_rate_percentage))

    # Define x-axis range dynamically based on MDE and sigma
    x_min = -(obj.min_detectable_effect_percentage / 100 + 4 * sigma)
    x = np.linspace(x_min, -x_min, 1000)

    # Define means for H₀ (null hypothesis) and H₁ (alternative hypothesis)
    mu_H0 = 0
    mu_MDE = obj.min_detectable_effect_percentage / 100

    # Generate normal distributions for H₀ and H₁
    H0_distribution = norm.pdf(x, mu_H0, sigma)
    MDE_distribution = norm.pdf(x, mu_MDE, sigma)

    # Create a Matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(14, 7), dpi=120)

    # Plot the distributions
    ax.plot(
        x,
        H0_distribution,
        color="#3838e7",  # Deep blue for H₀
        label="H₀: No Effect (Null Hypothesis)",
        linewidth=2,
    )
    ax.plot(
        x,
        MDE_distribution,
        color="#40e0d0",  # Turquoise for H₁
        label="H₁: Detectable Effect (Alternative Hypothesis)",
        linewidth=2,
    )

    # Dashed lines for means
    ax.axvline(mu_H0, color="#1a1a80", linestyle="--", linewidth=1.5, label="H₀ Mean")
    ax.axvline(mu_MDE, color="#26c2a4", linestyle="--", linewidth=1.5, label="H₁ Mean (MDE)")

    # Calculate critical values (z_alpha for significance level, z_beta for power)
    if obj.hypothesis == "One-sided Test":
        z_alpha = norm.ppf((100 - obj.alpha) / 100, mu_H0, sigma)
    else:
        z_alpha_right = norm.ppf(1 - obj.alpha / 200, mu_H0, sigma)
        z_alpha_left = norm.ppf(obj.alpha / 200, mu_H0, sigma)
    z_beta = norm.ppf((100 - obj.power) / 100, mu_MDE, sigma)

    # Highlight Type I and Type II Errors
    if obj.hypothesis == "One-sided Test":
        ax.fill_between(
            x,
            H0_distribution,
            where=(x > z_alpha),
            color="#3838e7",
            alpha=0.2,  # Slight transparency for Type I Error
            label="Type I Error (α)",
        )
    else:  # Two-sided Test
        ax.fill_between(
            x,
            H0_distribution,
            where=(x > z_alpha_right) | (x < z_alpha_left),
            color="#3838e7",
            alpha=0.2,  # Slight transparency for Type I Error
            label="Type I Error (α)",
        )

    ax.fill_between(
        x,
        MDE_distribution,
        where=(x < z_beta),
        color="#40e0d0",
        alpha=0.2,  # Slight transparency for Type II Error
        label="Type II Error (β)",
    )

    # Adjust axis limits and labels
    ax.set_xlim(x_min, -x_min)
    ax.set_ylim(0, max(H0_distribution.max(), MDE_distribution.max()) * 1.2)
    ax.set_xlabel("Effect Size", fontsize=16, fontweight="bold")
    ax.set_ylabel("Density", fontsize=16, fontweight="bold")
    ax.set_title(
        "Hypothesis Testing: Null vs Alternative Hypotheses",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    ax.text(
        0,
        -0.05,
        "This plot illustrates the Null and Alternative Hypotheses with critical regions for statistical errors.",
        ha="center",
        fontsize=12,
        color="gray",
    )

    # Customize legend
    ax.legend(
        loc="upper right",
        frameon=True,
        fancybox=True,
        shadow=True,
        fontsize=12,
        borderpad=1,
    )

    # Add a grid
    ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.7)

    # Add padding around the plot
    plt.tight_layout(pad=3)

    # Return the figure object
    return fig
