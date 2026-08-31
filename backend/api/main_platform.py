"""Production API entry: AGR engine plus open-land platform routes.

Use: uvicorn api.main_platform:app
`api.main:app` remains the core AGR service; this module attaches the
platform catalogue, VDL overlay, gaps, downloads, and place context.
"""

from __future__ import annotations

from api import main as core
from api.main import app
from api.platform_routes import router
from layers.platform import place_context

app.include_router(router)

_orig_square = core._square_response


def _square_with_platform(*args, **kwargs):
    payload = _orig_square(*args, **kwargs)
    square = payload["square"]
    agr = payload.get("agr") or {}
    plot_gbp = agr.get("roll_annual_rent_notional_plot_gbp") or 0.0
    if plot_gbp < 1500:
        value_band = "low"
    elif plot_gbp < 4500:
        value_band = "mid"
    else:
        value_band = "high"
    context = place_context(
        square["lat"],
        square["lng"],
        parcel=payload.get("parcel"),
    )
    context["filters"]["value_band"] = value_band
    context["filters"]["value_band_plot_gbp"] = plot_gbp
    payload["platform"] = context
    return payload


core._square_response = _square_with_platform
