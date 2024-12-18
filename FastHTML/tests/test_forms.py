import pytest
from src.a_btest.FastHTML.forms import (
    sample_size_calculator_form,
    visualization_tab,
    data_analysis_tab,
)
from fasthtml.common import Div


def test_sample_size_calculator_form():
    form = sample_size_calculator_form()
    assert form is not None, "Form should not be None."
    assert hasattr(form, "render"), "The form should have a 'render' method."
    assert "Baseline Metric" in form.render(), "Baseline Metric input not found."


def test_visualization_tab():
    form = visualization_tab()
    assert form is not None, "Visualization tab should not be None."
    assert hasattr(form, "render"), "The visualization tab should have a 'render' method."
    assert "Baseline Conversion Rate (%)" in form.render(), "Baseline Conversion Rate input not found."


def test_data_analysis_tab():
    form = data_analysis_tab()
    assert form is not None, "Data analysis tab should not be None."
    assert hasattr(form, "render"), "The data analysis tab should have a 'render' method."
    assert "Weekly Traffic" in form.render(), "Weekly Traffic input not found."
