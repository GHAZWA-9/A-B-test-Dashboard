from typing import Annotated
from fastapi import FastAPI, Form, Request, Response, Query, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import io  # For handling byte streams
from src.a_btest.API.APIModels import (
    DurationParameter,
    CalculateResponseDuration,
    Mde_Parameter,
    TableRow,
    VisualParameter,
)
import uvicorn
from function_estimation import *

# import subprocess

# from a_btest.estimation_binomial import ABTEST

app = FastAPI()
# don't declare app here and coonect it to the fasthtml server
# templates = Jinja2Templates(directory="/Users/hedlighazwa/Desktop/a-btest/src/a_btest/templates")
# app.mount("/static", StaticFiles(directory="/Users/hedlighazwa/Desktop/a-btest/src/a_btest/static"), name="static")


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/calculate_sample_size")
async def calculate_SZ(duration_Parameter: Annotated[DurationParameter, Depends()]) -> CalculateResponseDuration:

    sample_size, duration_days = get_sz_duration(duration_Parameter)
    return CalculateResponseDuration(sample_size=sample_size, duration_days=duration_days)


# toto.kameleoon.com/visualize?number_of_variants=2&min_detectable_effect=0.1&significance_level=0.05&beta=0.2&baseline_conversion_rate=0.1&control_allocation=0.5&variant_allocations=0.3,0.2
@app.get("/vizualize")
async def vizualize(visualPa: Annotated[VisualParameter, Depends()]) -> Response:
    # Create an instance of Estimation with the provided form data

    fig = generate_plot(visualPa)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    # Return image as response
    return Response(content=buf.getvalue(), media_type="image/png")


@app.get("/get_table_mde")
async def get_table(mde_Parameter: Annotated[Mde_Parameter, Depends()]) -> list[TableRow]:

    weeks = mde_Parameter.number_weeks  # For example, generate data for 5 weeks
    results = []
    var = mde_Parameter.weekly_visitors
    for week in range(1, weeks + 1):

        mde_Parameter.weekly_visitors = var * week
        mde = calculate_mde(mde_Parameter)
        duration_parameter = DurationParameter(
            significance_level=5,
            beta=20,
            number_of_variants=mde_Parameter.number_of_variants,
            min_detectable_effect_percentage=mde * 100,
            daily_visitors=1000,
            baseline_conversion_rate=mde_Parameter.weekly_conversions / var,
            control_allocation=50,
            variant_allocations=[50],
        )
        visitors = get_sz_duration(duration_parameter)[0]

        results.append(TableRow(week=week, mde=round(mde, 3), visitors=visitors))
    return results


if __name__ == "__main__":
    uvicorn.run("APIconfig:app", host="0.0.0.0", port=8000, reload=True)
