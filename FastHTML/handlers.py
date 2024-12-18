"""
A/B Test Dashboard Side Functions

This module defines the Side functionalities for the A/B Test Dashboard.
It includes:
1. Data analysis calculations
2. Plot generation for power analysis
3. Sample size calculation
4. Dynamic field updates for metric type and allocations

Each function is designed to handle specific aspects of the A/B testing workflow.
"""

import pandas as pd
from fasthtml.common import *
from src.a_btest.function_estimation import *
from src.a_btest.API.APIModels import Mde_Parameter, BinomialParameters
from io import BytesIO
import base64
import matplotlib.pyplot as plt


async def post_data_analysis(req):
    # Retrieve the form data
    form_data = await req.form()

    # Extract form values from the form submission
    weekly_traffic = int(form_data.get("weekly_traffic", 1000))
    weekly_conversions = int(form_data.get("weekly_conversions", 50))
    num_variants = int(form_data.get("num_variants", 2))

    # Calculate baseline conversion rate
    baseline_cr = round(weekly_conversions / weekly_traffic, 2)
    alpha = 5  # Significance level
    beta = 20  # Statistical power

    # Prepare results list for analysis
    results = []

    # Loop through 1 to 5 weeks to perform calculations
    for weeks in range(1, 6):
        # Mde_Parameter setup for calculating the MDE
        mde_params = Mde_Parameter(
            number_of_variants=num_variants,
            significance_level=alpha,
            beta=beta,
            weekly_visitors=weekly_traffic * weeks,
            weekly_conversions=weekly_conversions * weeks,
        )

        # Calculate MDE (Minimum Detectable Effect)
        mde = calculate_mde(mde_params)

        # DurationParameter setup for calculating sample size and duration
        duration_params = BinomialParameters(
            number_of_variants=num_variants,
            min_detectable_effect_percentage=mde * 100,  # Convert to percentage
            significance_level=alpha,
            beta=beta,
            baseline_metric=baseline_cr * 100,
            control_allocation=50,
            variant_allocations=50,
            daily_visitors=weekly_traffic,  # Using weekly_traffic
        )

        # Get sample size and duration
        visitors, duration = get_sz_duration(duration_params)

        # Append calculated result for each week
        results.append(
            {
                "N° week": weeks,
                "Minimum Detectable Effect": f"{mde * 100:.2f}",
                "Visitors per variant": int(visitors),
            }
        )

    # Create the table header with tooltip for MDE
    table_header = Tr(
        Th("N° week", cls="table-header"),
        Th(
            Div(
                "Minimum Detectable Effect",
                Div(
                    "This value represents the smallest effect size that can be reliably detected.",
                    cls="tooltip-content",
                ),
                cls="tooltip-container",
            ),
            cls="table-header",
        ),
        Th("Visitors per variant", cls="table-header"),
    )

    # Create table rows with alternating classes
    table_rows = []

    for index, result in enumerate(results):
        if index % 2 == 0:
            ch = "cell-odd"
        else:
            ch = "cell-even"
        table_rows.append(
            Tr(
                Td(str(result["N° week"]), cls=ch),
                Td(result["Minimum Detectable Effect"], cls=ch),
                Td(str(result["Visitors per variant"]), cls=ch),
                cls=ch,  # Alternating row styles
            )
        )

    # Wrap the table in a styled container
    table = Div(
        Table(table_header, *table_rows, cls="custom-data-table"),  # Main CSS class for the table
    )

    # Return the styled table in the result area
    return Div(
        table,
        id="data-analysis-result",
    )


async def generate_plot_bis(req):
    form_data = await req.form()

    # Extract data from the form
    baseline_conversion = float(form_data.get("baseline_metric_average", 1)) / 100
    minimum_effect = float(form_data.get("minimum_effect", 1)) / 100
    test_type = form_data.get("test_type", "One-sided Test")
    alpha = float(form_data.get("alpha (%)", 5))
    beta = float(form_data.get("beta (%)", 80))

    # Placeholder: ABTEST class and plot generation logic
    obj = VisualParameter(alpha=alpha, power=beta, hypothesis=test_type, min_detectable_effect_percentage=minimum_effect, baseline_conversion_rate_percentage=baseline_conversion)

    fig = generate_plot(obj)  # Generate plot using the calculator

    # Save the plot to a PNG image
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    # Embed the image in the response
    return Div(
        Img(src=f"data:image/png;base64,{plot_data}", style="width: 100%; height: 100%; display: block; object-fit: cover; margin: 0;"),
        id="plot-container",
        cls="plot-area",  # Ensures the Div container also fills the entire result area
    )


async def calculate_sample_size(req):
    sample_size = None
    form_data = await req.form()
    metric_type = form_data.get("metric_type", "binomial")
    allocations = []
    # Iterate over form data keys to find allocations
    for key, value in form_data.items():
        if key.startswith("variant_"):
            # Ensure value is not None or empty
            allocations.append(float(value))
    # Trouver la valeur minimale parmi toutes les allocations
    min_allocation = min(allocations) if allocations else 0
    if metric_type == "binomial":
        duration_parameter = BinomialParameters(
            beta=float(form_data.get("beta", 80)),
            significance_level=float(form_data.get("significance_level", 5)),
            min_detectable_effect_percentage=float(form_data.get("mde", 20)),
            baseline_metric=float(form_data.get("baseline_metric_average", 10)),
            control_allocation=float(form_data.get("control_allocation", 50)),
            variant_allocations=min_allocation,
            daily_visitors=float(form_data.get("daily_visitors", 1000)),
            hypothesis=form_data.get("hypothesis", "One-sided Test"),
        )
    else:
        duration_parameter = ContinuousParameters(
            beta=float(form_data.get("beta", 80)),
            significance_level=float(form_data.get("significance_level", 5)),
            min_detectable_effect_percentage=float(form_data.get("mde", 20)),
            baseline_metric=float(form_data.get("baseline_metric_average", 10)),
            control_allocation=float(form_data.get("control_allocation", 50)),
            variant_allocations=min_allocation,
            daily_visitors=float(form_data.get("daily_visitors", 1000)),
            hypothesis="One-sided Test",
            std=float(form_data.get("std", 10)),
        )

    # Get the sample size and duration
    sample_size, duration = get_sz_duration(duration_parameter)
    if sample_size == None:
        return Div(
            Div(
                P("Sample Size", cls="result-label"),
                H3("--", id="sample-size-value", cls="result-value"),
                cls="result-block result-block-top",
            ),
            Div(
                P(" Duration (days)", cls="result-label"),
                H3("--", id="duration-value", cls="result-value"),
                cls="result-block result-block-bottom",
            ),
            id="result-container",  # ID correspondant au conteneur cible
            cls="result-half",
        )
    # Dynamically update the result section
    else:

        return Div(
            Div(
                P("Sample Size", cls="result-label"),
                H3(f"{sample_size:,.0f}", id="sample-size-value", cls="result-value"),
                cls="result-block result-block-top",
            ),
            Div(
                P(" Duration (days)", cls="result-label"),
                H3(f"{duration:.0f}", id="duration-value", cls="result-value"),
                cls="result-block result-block-bottom",
            ),
            id="result-container",  # ID correspondant au conteneur cible
            cls="result-half",
        )


def update_allocations(num_variants: int):
    variant_inputs = create_variant_inputs(num_variants)
    return variant_inputs


# Function to create dynamic input fields for variant allocations
def create_variant_inputs(num_variants):
    fields = [
        Div(
            Label("Control Allocation (%)"),
            Input(
                name="control_allocation",
                type="number",
                min="0",
                max="100",
                step="0.01",
                required=True,
                cls="form-control",
            ),
            cls="form-group",
        )
    ]
    for i in range(1, num_variants):
        fields.append(
            Div(
                Label(f"Variant {i} Allocation (%)"),
                Input(
                    name=f"variant_{i}_allocation",
                    type="number",
                    min="0",
                    max="100",
                    step="0.01",
                    required=True,
                    cls="form-control",
                ),
                cls="form-group",
            )
        )
    return Div(*fields, id="allocations-container", cls="allocation-container")


def update_metric_fields(metric_type: str):
    # Champs par défaut : Alpha et Beta avec tooltips
    fields = [
        Div(
            Div(
                Div(
                    Label(
                        "Alpha (%)",
                        cls="label-with-tooltip",  # Align text and tooltip horizontally
                    ),
                    Div(
                        Label("?", cls="tooltip-icon"),  # Tooltip icon
                        Div(
                            "Significance level in percentage (probability of Type I error).",
                            cls="tooltip-content",
                        ),
                        cls="tooltip-container",  # Tooltip container for alignment
                    ),
                    cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                ),
                Input(
                    id="alpha",
                    name="alpha",
                    type="number",
                    step="0.01",
                    value="5",
                    cls="form-control",
                    required=True,
                ),
                cls="form-group",
            ),
            Div(
                Div(
                    Label(
                        "Beta (%)",
                        cls="label-with-tooltip",  # Align text and tooltip horizontally
                    ),
                    Div(
                        Label("?", cls="tooltip-icon"),  # Tooltip icon
                        Div(
                            "Statistical power complement (probability of Type II error).",
                            cls="tooltip-content",
                        ),
                        cls="tooltip-container",  # Tooltip container for alignment
                    ),
                    cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                ),
                Input(
                    id="beta",
                    name="beta",
                    type="number",
                    step="0.01",
                    value="20",
                    cls="form-control",
                    required=True,
                ),
                cls="form-group",
            ),
            cls="d-flex flex-equal two-fields",  # Deux champs alignés sur deux colonnes
        )
    ]

    # Si le type de métrique est "continuous", ajoutez le champ Std avec un tooltip
    if metric_type == "continuous":
        std_field = Div(
            Div(
                Label(
                    "Std",
                    cls="label-with-tooltip",  # Align text and tooltip horizontally
                ),
                Div(
                    Label("?", cls="tooltip-icon"),  # Tooltip icon
                    Div(
                        "Standard deviation of the continuous metric.",
                        cls="tooltip-content",
                    ),
                    cls="tooltip-container",  # Tooltip container for alignment
                ),
                cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
            ),
            Input(
                id="std",
                name="std",
                type="number",
                step="0.01",
                value="10",
                cls="form-control",
                required=True,
            ),
            cls="form-group",
        )
        # Réorganiser en trois champs avec tooltips
        fields = [
            Div(
                Div(
                    Div(
                        Label(
                            "Alpha (%)",
                            cls="label-with-tooltip",  # Align text and tooltip horizontally
                        ),
                        Div(
                            Label("?", cls="tooltip-icon"),  # Tooltip icon
                            Div(
                                "Significance level in percentage (probability of Type I error).",
                                cls="tooltip-content",
                            ),
                            cls="tooltip-container",  # Tooltip container for alignment
                        ),
                        cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                    ),
                    Input(
                        id="alpha",
                        name="alpha",
                        type="number",
                        step="0.01",
                        value="5",
                        cls="form-control",
                        required=True,
                    ),
                    cls="form-group",
                ),
                Div(
                    Div(
                        Label(
                            "Beta (%)",
                            cls="label-with-tooltip",  # Align text and tooltip horizontally
                        ),
                        Div(
                            Label("?", cls="tooltip-icon"),  # Tooltip icon
                            Div(
                                "Statistical power complement (probability of Type II error).",
                                cls="tooltip-content",
                            ),
                            cls="tooltip-container",  # Tooltip container for alignment
                        ),
                        cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                    ),
                    Input(
                        id="beta",
                        name="beta",
                        type="number",
                        step="0.01",
                        value="20",
                        cls="form-control",
                        required=True,
                    ),
                    cls="form-group",
                ),
                std_field,  # Ajouter le champ Std avec tooltip
                cls="d-flex flex-equal three-fields",  # Trois champs alignés sur trois colonnes
            )
        ]

    return Div(*fields, id="metric-fields")
