"""
Form Definitions for AB Test Dashboard

This module contains the definitions of forms and tabs used in the AB Test Dashboard.
Each form is designed for a specific feature:

1. Sample Size Calculator
2. Traffic and Conversion Analysis
3. Power Analysis Visualization

Features include tooltips for user guidance, dynamic field updates, and interactive components.


"""

from fasthtml.common import *
from src.a_btest.FastHTML.handlers import calculate_sample_size


def sample_size_calculator_form():
    form = Form(
        Fieldset(
            # Baseline Metric Average %
            Div(
                Div(
                    Label(
                        "Baseline Metric",
                        cls="label-with-tooltip",  # Align text and tooltip horizontally
                    ),
                    Div(
                        Label("?", cls="tooltip-icon"),  # Tooltip icon
                        Div(
                            "Baseline metric in percentage.",  # Tooltip text
                            cls="tooltip-content",
                        ),
                        cls="tooltip-container",  # Tooltip container for alignment
                    ),
                    cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                ),
                Input(
                    id="baseline_metric_average",
                    placeholder="Enter baseline conversion rate",
                    value="20",
                    type="number",
                    step="0.01",
                    name="baseline_metric_average",
                    required=True,
                    cls="form-control",
                ),
                cls="form-group",
            ),
            # Daily Visitors
            Div(
                Div(
                    Label(
                        "Daily Visitors",
                        cls="label-with-tooltip",  # Align text and tooltip horizontally
                    ),
                    Div(
                        Label("?", cls="tooltip-icon"),  # Tooltip icon
                        Div(
                            "Number of visitors per day.",  # Tooltip text
                            cls="tooltip-content",
                        ),
                        cls="tooltip-container",  # Tooltip container for alignment
                    ),
                    cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                ),
                Input(
                    id="daily_visitors",
                    placeholder="Enter daily visitors",
                    value="1000",
                    type="number",
                    step="1",
                    name="daily_visitors",
                    required=True,
                    cls="form-control",
                ),
                cls="form-group",
            ),
            # Minimum Detectable Effect (MDE)
            Div(
                Div(
                    Label(
                        "Minimum Detectable Effect",
                        cls="label-with-tooltip",  # Align text and tooltip horizontally
                    ),
                    Div(
                        Label("?", cls="tooltip-icon"),  # Tooltip icon
                        Div(
                            "Smallest effect size that you want to detect, in % .",  # Tooltip text
                            cls="tooltip-content",
                        ),
                        cls="tooltip-container",  # Tooltip container for alignment
                    ),
                    cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                ),
                Input(
                    id="mde",
                    placeholder="Enter MDE",
                    value="20",
                    type="number",
                    step="0.01",
                    name="mde",
                    required=True,
                    cls="form-control",
                ),
                cls="form-group",
            ),
            # Type of Metric - Radio buttons
            Div(
                Div(
                    Label(
                        "Type of Metric",
                        cls="label-with-tooltip",  # Align text and tooltip horizontally
                    ),
                    Div(
                        Label("?", cls="tooltip-icon"),  # Tooltip icon
                        Div(
                            "Choose the type of metric: discrete or continuous.",  # Tooltip text
                            cls="tooltip-content",
                        ),
                        cls="tooltip-container",  # Tooltip container for alignment
                    ),
                    cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                ),
                Div(
                    Div(
                        Input(
                            type="radio",
                            id="discrete",
                            name="metric_type",
                            value="discrete",
                            _hx_post="/update-metric-fields",
                            _hx_target="#metric-fields",
                            _hx_include="[name=metric_type]",
                            checked=True,  # Default selection
                            cls="radio-input",
                        ),
                        Label("Discrete", _for="discrete", cls="radio-label"),
                        cls="radio-option",  # Individual button-style container
                    ),
                    Div(
                        Input(
                            type="radio",
                            id="continuous",
                            name="metric_type",
                            value="continuous",
                            _hx_post="/update-metric-fields",
                            _hx_target="#metric-fields",
                            _hx_include="[name=metric_type]",
                            cls="radio-input",
                        ),
                        Label("Continuous", _for="continuous", cls="radio-label"),
                        cls="radio-option",  # Individual button-style container
                    ),
                    cls="radio-options-container",  # Holds both buttons horizontally
                ),
                cls="form-group",
                style="margin-bottom: 10px;",  # Add spacing below the radio buttons
            ),
            # Conteneur pour les champs Alpha, Beta, et Std
            Div(
                id="metric-fields",  # ID du conteneur à mettre à jour
                cls="form-group",
                _hx_post="/update-metric-fields",  # Charge les champs par défaut
                _hx_trigger="load",  # Charger les champs par défaut
                _hx_target="#metric-fields",
                _hx_include="[name=metric_type]",
                _hx_swap="outerHTML",
            ),
            # Number of Variants
            Div(
                Div(
                    Label(
                        "Number of Variants",
                        cls="label-with-tooltip",  # Align text and tooltip horizontally
                    ),
                    Div(
                        Label("?", cls="tooltip-icon"),  # Tooltip icon
                        Div(
                            "Number of groups or variations in your experiment.",  # Tooltip text
                            cls="tooltip-content",
                        ),
                        cls="tooltip-container",  # Tooltip container for alignment
                    ),
                    cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                ),
                Input(
                    id="num_variants",
                    type="number",
                    min="2",
                    step="1",
                    name="num_variants",
                    required=True,
                    _hx_post="/update-allocations",  # Triggers dynamic variant allocations
                    _hx_target="#allocation-fields",
                    _hx_swap="innerHTML",
                    cls="form-control",
                ),
                cls="form-group",
            ),
            # Placeholder for dynamic allocation fields
            Div(id="allocation-fields", cls="form-group"),
        ),
        Div(
            Button(
                "Calculate Sample Size",
                type="submit",
                cls="btn btn-success",
                _hx_post="/calculate_sample_size",
                _hx_target="#result-container",
                _hx_swap="outerHTML",
            ),
            cls="form-group",
        ),
    )
    # Section des résultats par défaut avec "--"
    result_section = Div(
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

    # Retour complet : formulaire + conteneur de résultats
    return Div(form, result_section, cls="sample-size-container")


def data_analysis_tab():
    form = Div(
        Form(
            Fieldset(
                Div(
                    Div(
                        Label("Weekly Traffic", cls="label-with-tooltip"),
                        Div(
                            Label("?", cls="tooltip-icon"),  # Tooltip icon
                            Div(
                                "Enter the number of visitors to your website per week.",  # Tooltip description
                                cls="tooltip-content",
                            ),
                            cls="tooltip-container",  # Tooltip container for alignment
                        ),
                        cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                    ),
                    Input(
                        id="weekly_traffic",
                        type="number",
                        name="weekly_traffic",
                        placeholder="Enter weekly traffic",
                        min="100",
                        step="100",
                        required=True,
                        cls="form-control",  # Classe identique à sample_size_form
                    ),
                    cls="form-group",  # Classe identique à sample_size_form
                ),
                Div(
                    Div(
                        Label("Weekly Conversions", cls="label-with-tooltip"),
                        Div(
                            Label("?", cls="tooltip-icon"),  # Tooltip icon
                            Div(
                                "Enter the number of successful conversions per week.",
                                cls="tooltip-content",
                            ),
                            cls="tooltip-container",  # Tooltip container for alignment
                        ),
                        cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                    ),
                    Input(
                        id="weekly_conversions",
                        type="number",
                        name="weekly_conversions",
                        placeholder="Enter weekly conversions",
                        min="1",
                        step="1",
                        required=True,
                        cls="form-control",  # Classe identique à sample_size_form
                    ),
                    cls="form-group",  # Classe identique à sample_size_form
                ),
                Div(
                    Div(
                        Label("Number of Variants", cls="label-with-tooltip"),
                        Div(
                            Label("?", cls="tooltip-icon"),  # Tooltip icon
                            Div(
                                "Enter the number of A/B test variants, including the control group.",
                                cls="tooltip-content",
                            ),
                            cls="tooltip-container",  # Tooltip container for alignment
                        ),
                        cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                    ),
                    Input(
                        id="num_variants",
                        type="number",
                        value="2",
                        min="2",
                        step="1",
                        name="num_variants",
                        required=True,
                        cls="form-control",  # Classe identique à sample_size_form
                    ),
                    cls="form-group",  # Classe identique à sample_size_form
                ),
                Div(
                    Button(
                        "Calculate",
                        type="submit",
                        cls="btn",  # Bouton identique
                        _hx_post="/calculate_data_analysis",
                        _hx_target="#data-analysis-result",
                        _hx_swap="outerHTML",
                    ),
                    cls="form-group",  # Aligner le bouton identique à sample_size_form
                    style="text-align: center; margin-top: 1%;",
                ),
            ),
        ),
        cls="form-group",  # Classe alignée sur celle de sample_size_form
    )

    # Section des résultats
    result_section = Div(
        Div(
            id="data-analysis-result",
            cls="result-area",  # Même classe pour harmoniser les résultats
            style="padding: 0; margin: 0; overflow: hidden; display: flex; justify-content: center;",
        ),  # Alignement identique à sample_size_form
    )

    # Conteneur principal
    return Div(
        form,
        result_section,
        cls="sample-size-container",  # Conteneur principal harmonisé avec sample_size_form
    )


def visualization_tab():
    # Formulaire utilisateur pour entrer les paramètres
    form = Div(
        Form(
            Fieldset(
                # Baseline Conversion Rate
                Div(
                    Div(
                        Label("Baseline Conversion Rate", cls="label-with-tooltip"),
                        Div(
                            Label("?", cls="tooltip-icon"),  # Tooltip icon
                            Div(
                                "The percentage of users who convert in the control group.",
                                cls="tooltip-content",
                            ),
                            cls="tooltip-container",  # Tooltip container for alignment
                        ),
                        cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                    ),
                    Input(
                        id="baseline_metric_average",  # Correspond à generate_plot_bis
                        type="number",
                        min="1",
                        max="100",
                        step="0.01",
                        placeholder="Enter baseline conversion rate",
                        required=True,
                        cls="form-control",
                    ),
                    cls="form-group",
                ),
                # Minimum Detectable Effect
                Div(
                    Div(
                        Label("Minimum Detectable Effect", cls="label-with-tooltip"),
                        Div(
                            Label("?", cls="tooltip-icon"),  # Tooltip icon
                            Div(
                                "The smallest difference in conversion rates you want to detect.",
                                cls="tooltip-content",
                            ),
                            cls="tooltip-container",  # Tooltip container for alignment
                        ),
                        cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                    ),
                    Input(
                        id="minimum_effect",  # Correspond à generate_plot_bis
                        type="number",
                        min="0.01",
                        max="100",
                        step="0.01",
                        placeholder="Enter minimum detectable effect",
                        required=True,
                        cls="form-control",
                    ),
                    cls="form-group",
                ),
                # Hypothesis Selection with Tooltip
                Div(
                    Div(
                        Label("Hypothesis", cls="label-with-tooltip"),
                        Div(
                            Label("?", cls="tooltip-icon"),  # Tooltip icon
                            Div(
                                "Choose one-sided or two-sided test based on your hypothesis.",
                                cls="tooltip-content",  # Tooltip text
                            ),
                            cls="tooltip-container",  # Tooltip container for alignment
                        ),
                        cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                    ),
                    Div(
                        Div(
                            Input(
                                type="radio",
                                id="one_sided",
                                name="test_type",
                                value="One-sided Test",
                                checked=True,  # Default selection
                                cls="radio-input",  # Hidden native radio input
                            ),
                            Label(
                                "One-side test (Recommended)",
                                _for="one_sided",
                                cls="radio-label-vertical",  # Styled label for vertical alignment
                            ),
                            Div(
                                "Determines if the test variation is better than the control.",
                                cls="radio-description-vertical",  # Description below the label
                            ),
                            cls="radio-option-vertical",  # Wrapper for each radio option (vertical alignment)
                        ),
                        Div(
                            Input(
                                type="radio",
                                id="two_sided",
                                name="test_type",
                                value="Two-sided Test",
                                cls="radio-input",  # Hidden native radio input
                            ),
                            Label(
                                "Two-side test",
                                _for="two_sided",
                                cls="radio-label-vertical",  # Styled label for vertical alignment
                            ),
                            Div(
                                "Determines if the test variation is different than the control.",
                                cls="radio-description-vertical",  # Description below the label
                            ),
                            cls="radio-option-vertical",  # Wrapper for each radio option (vertical alignment)
                        ),
                        cls="radio-container-vertical",  # Wrapper for both radio options
                    ),
                    cls="form-group",
                ),
                # Significance Level and Statistical Power
                Div(
                    Div(
                        Div(
                            Label("Significance Level", cls="label-with-tooltip"),
                            Div(
                                Label("?", cls="tooltip-icon"),  # Tooltip icon
                                Div(
                                    "The probability of rejecting the null hypothesis when it is true.",
                                    cls="tooltip-content",
                                ),
                                cls="tooltip-container",  # Tooltip container for alignment
                            ),
                            cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                        ),
                        Input(
                            id="alpha",
                            name="alpha",  # Correspond à generate_plot_bis
                            type="number",
                            min="0.01",
                            max="10.0",
                            step="0.01",
                            placeholder="5",
                            required=True,
                            cls="form-control",  # Valeur par défaut cohérente
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Div(
                            Label("Statistical Power", cls="label-with-tooltip"),
                            Div(
                                Label("?", cls="tooltip-icon"),  # Tooltip icon
                                Div(
                                    "The probability of detecting a true effect (1 - β).",
                                    cls="tooltip-content",
                                ),
                                cls="tooltip-container",  # Tooltip container for alignment
                            ),
                            cls="label-tooltip-wrapper",  # Wrapper for label and tooltip
                        ),
                        Input(
                            id="beta",
                            name="beta",  # Correspond à generate_plot_bis
                            type="number",
                            min="65.0",
                            max="95.0",
                            step="0.01",
                            placeholder="80",
                            required=True,
                            cls="form-control",
                        ),
                        cls="form-group",
                    ),
                    cls="d-flex flex-equal two-fields",  # Les deux champs côte à côte
                ),
                # Submit Button
                Div(
                    Button(
                        "Generate Plot",
                        type="submit",
                        cls="btn",
                        _hx_post="/generate-plot",  # Assure la synchronisation avec la route de generate_plot_bis
                        _hx_target="#plot-container",
                        _hx_swap="innerHTML",
                    ),
                    cls="form-group",
                    style="text-align: center; margin-top: 2%;",
                ),
            )
        ),
        cls="form-container",  # Alignement avec sample_size_form
    )

    # Conteneur pour le graphique avec un cadre stylisé
    plot_section = Div(
        id="plot-container",
        cls="img",  # Classe identique pour harmoniser les résultats
    )

    # Retourner le formulaire et le graphique côte à côte
    return Div(form, plot_section, cls="sample-size-container")
