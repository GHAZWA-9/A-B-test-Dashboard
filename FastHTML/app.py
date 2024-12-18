"""
AB Test Dashboard Application

This script defines the main routes and application logic for the AB Test Dashboard.
The dashboard provides tools for:
1. Sample Size Calculation
2. Traffic & Conversion Analysis
3. Power Analysis Visualization

The application uses FastHTML for UI rendering and interaction and includes the following features:
- Dynamically loaded tabs with forms and visualizations.
- Real-time updates via HTMX integration.
- Server-side calculation and visualization generation.

Routes:
- `/`: Main page with tab navigation.
- `/sample-size-calculator`: Displays the sample size calculator form.
- `/visualization`: Displays the power analysis visualization form.
- `/data-analysis`: Displays the traffic and conversion analysis form.
- `/calculate_data_analysis`: Handles the analysis logic for the data analysis tab.
- `/generate-plot`: Handles plot generation for the power analysis tab.
- `/calculate_sample_size`: Processes the sample size calculation form.
- `/update-allocations`: Updates dynamic fields for variant allocations.
- `/update-metric-fields`: Updates dynamic metric fields based on the selected metric type.
"""

import pandas as pd
from fasthtml.common import Style, Titled, Div, Button, serve, fast_app
from src.a_btest.API.APIModels import *
from src.a_btest.FastHTML.forms import sample_size_calculator_form, data_analysis_tab, visualization_tab
from src.a_btest.FastHTML.handlers import calculate_sample_size, update_allocations, update_metric_fields, post_data_analysis, generate_plot_bis


# Charger le style CSS
with open("src/a_btest/FastHTML/style.css", "r") as file:
    css_code = file.read()

app, rt = fast_app(hdrs=(Style(css_code),))


# Définition des routes principales
@rt("/")
def get():
    # Rendu initial avec le premier onglet ("Sample Size") act
    return Titled(
        "",
        Div(
            Div(
                Button("Sample Size", _hx_get="/sample-size-calculator", _hx_target="#tab-content", _hx_swap="innerHTML"),
                Button("Traffic & Conversion", _hx_get="/data-analysis", _hx_target="#tab-content", _hx_swap="innerHTML"),
                Button("Power Analysis", _hx_get="/visualization", _hx_target="#tab-content", _hx_swap="innerHTML"),
                cls="tab-buttons",
            ),
            Div(id="tab-content", cls="main-container"),
        ),
    )


@rt("/sample-size-calculator")
def get_sample_size_calculator():
    return sample_size_calculator_form()


@rt("/visualization")
def get_visualization():
    return visualization_tab()


@rt("/data-analysis")
def get_data_analysis():
    return data_analysis_tab()


@rt("/calculate_data_analysis")
async def calculate_data_analysis(req):
    return await post_data_analysis(req)


@rt("/generate-plot")
async def generate_visualization_plot(req):
    return await generate_plot_bis(req)


@rt("/calculate_sample_size")
async def calculate_sample_size_route(req):
    return await calculate_sample_size(req)


@rt("/update-allocations")
def update_allocations_route(num_variants: int):
    return update_allocations(num_variants)


@rt("/update-metric-fields")
def update_metric_fields_route(metric_type: str):
    return update_metric_fields(metric_type)


# Lancer l'application
serve(app="app", host="0.0.0.0", port=5001)
