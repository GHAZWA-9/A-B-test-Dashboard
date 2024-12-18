from typing import List, Literal, Union
from pydantic import BaseModel, PositiveInt, Field, PositiveFloat
from fastapi import Query


class Parameter(BaseModel):
    significance_level: float = Field(5, ge=0, le=100)
    beta: float = Field(20, ge=0, le=100)
    number_of_variants: int = Field(2, ge=1, description="Number of  all variants")


class DurationParameterBase(Parameter):
    metric_type: Literal["binomial", "continuous"] = Field("binomial", description="Type of metric")
    min_detectable_effect_percentage: float = Field(20, ge=0, description="Minimum detectable effect (%)")
    daily_visitors: PositiveInt = Field(1000, description="Average Daily visitors ")
    control_allocation: float = Field(50, ge=0, le=100)
    baseline_metric: PositiveFloat = Field(0, ge=0)

    variant_allocations: float = Field(50, ge=0, le=100)  # give the min directly
    hypothesis: Literal["One-sided Test", "Two-sided Test"] = Field("One-sided Test", description="comparison Region test type")


class BinomialParameters(DurationParameterBase):
    metric_type: Literal["binomial"] = Field("binomial")


class ContinuousParameters(DurationParameterBase):

    metric_type: Literal["continuous"] = Field("continuous")
    std: float


DurationParameter = Union[BinomialParameters, ContinuousParameters]


class Mde_Parameter(Parameter):

    weekly_visitors: PositiveInt = Field(1000)
    weekly_conversions: PositiveInt = Field(200)
    number_weeks: PositiveInt = Field(5)


class CalculateResponseDuration(BaseModel):
    sample_size: int
    duration_days: int


class TableRow(BaseModel):
    week: PositiveInt  # Number of weeks
    mde: float  # Min. Det.Effect (MDE) %
    visitors: PositiveInt  # Visitors per variant

    # ENCODAGE JSON
    """ class Config:
        json_encoders = {float: lambda v: format(v, ".2f")"""

    """class CalculateResponseMde(BaseModel):
    data: List[TableRow]"""


class VisualParameter(BaseModel):
    alpha: float = Field(5, ge=0.000, le=100.000, description="Significance level (%), typically set at 5%")
    power: float = Field(80, ge=0.000, le=100.000, description="The desired statistical power of the test (%), typically set at 80%")
    hypothesis: Literal["One-sided Test", "Two-sided Test"] = Field("One-sided Test", description="comparison Region test type")
    min_detectable_effect_percentage: float = Field(20, ge=0.000, description="The minimum effect size that can be detected, (%)")
    baseline_conversion_rate_percentage: float = Field(10, ge=0.000, le=100.0000, description="The baseline conversion rate, (%)")
