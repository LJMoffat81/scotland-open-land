"""Open land platform layer catalog, place context, and official links.

The product brief is docs/PLATFORM.md. This module exposes what can be
shown from open sources and makes remaining registers visible as gaps.
"""

from __future__ import annotations

from typing import Any

from layers.council_metrics import METRIC_DEFS
from layers.vdl import query_point as vdl_at_point
from spatial.parcels import lookup_parcel_geojson

SCOTLIS_PUBLIC = "https://scotlis.ros.gov.uk/"
SCOTLIS_ABOUT = "https://www.ros.gov.uk/scotlis"
PUBLIC_LAND_MAP = "https://www.arcgis.com/apps/dashboards/a10668ccd4784209bf22e3adcef6b897"
VDL_REGISTER = (
    "https://www.gov.scot/publications/the-scottish-vacant-and-derelict-land-survey-site-register/"
)
SPATIAL_HUB_VDL = "https://data.spatialhub.scot/dataset/vacant_and_derelict_land-is"
SPATIAL_HUB_CAT = "https://data.spatialhub.scot/dataset/community_asset_transfer_register-is"
SPATIAL_HUB_ASSETS = "https://data.spatialhub.scot/dataset/council_asset_register-is"
SPATIAL_HUB_LA_OWN = "https://data.spatialhub.scot/dataset/land_ownership-is"
CROWN_ESTATE_HUB = "https://crown-estate-scotland-spatial-hub-coregis.hub.arcgis.com/"


def scotlis_links(lat: float, lng: float, postcode: str | None = None) -> dict[str, Any]:
    """Official title-sheet path. ScotLIS has no public coordinate deep-link API."""
    return {
        "label": "Official title on ScotLIS",
        "public_home": SCOTLIS_PUBLIC,
        "about": SCOTLIS_ABOUT,
        "note": (
            "ScotLIS is Registers of Scotland’s official land information service. "
            "Use it for title sheets, owners on the Land Register, and paid extracts. "
            "This platform does not replace ScotLIS."
        ),
        "search_hint": postcode or f"{lat:.5f}, {lng:.5f}",
    }


def platform_catalog() -> dict[str, Any]:
    return {
        "version": 2,
        "brief": "docs/PLATFORM.md",
        "principle": "AGR first — open layers around a residual land-rent engine.",
        "choropleth_metrics": [
            {
                "id": mid,
                **{k: v for k, v in defn.items() if k != "property"},
                "property": defn["property"],
            }
            for mid, defn in METRIC_DEFS.items()
        ],
        "layers": [
            {
                "id": "agr_value",
                "group": "value",
                "status": "live",
                "label": "Annual Ground Rent",
                "description": "Residual site-value AGR on W3W cells and notional plots.",
            },
            {
                "id": "boundaries",
                "group": "spatial",
                "status": "live",
                "label": "ROS INSPIRE parcels",
                "description": "Registered cadastral extents (geometry only — no owners).",
                "minzoom": 14,
            },
            {
                "id": "cell_grid",
                "group": "value",
                "status": "live",
                "label": "W3W cell grid",
                "minzoom": 12,
            },
            {
                "id": "vdl",
                "group": "spatial",
                "status": "live",
                "label": "Vacant and derelict land",
                "description": "SVDLS sites (survey polygons). Owner class is not legal title.",
                "endpoint": "/layers/open/vdl",
                "licence": "OGL-3.0",
                "source_url": VDL_REGISTER,
            },
            {
                "id": "public_crown",
                "group": "ownership",
                "status": "linked",
                "label": "Public and Crown Estate land",
                "description": (
                    "Scottish Government national map of selected public bodies and "
                    "Crown Estate Scotland. Linked until an OGL bulk extract is stored here."
                ),
                "source_url": PUBLIC_LAND_MAP,
            },
            {
                "id": "la_holdings",
                "group": "ownership",
                "status": "gap",
                "label": "Local-authority land holdings",
                "description": (
                    "Spatial Hub ‘Land Ownership – Scotland’ is not an open public layer "
                    "(PSGA / other restrictions). Shown as a gap, not scraped."
                ),
                "source_url": SPATIAL_HUB_LA_OWN,
            },
            {
                "id": "council_assets",
                "group": "ownership",
                "status": "gap",
                "label": "Council asset / CAT registers",
                "description": "Improvement Service amalgamated registers — Spatial Hub login.",
                "source_url": SPATIAL_HUB_ASSETS,
                "also": SPATIAL_HUB_CAT,
            },
            {
                "id": "common_good",
                "group": "ownership",
                "status": "gap",
                "label": "Common Good registers",
                "description": "Statutory LA registers; no single open national spatial layer yet.",
            },
            {
                "id": "sasine_private",
                "group": "ownership",
                "status": "gap",
                "label": "Private owners and Sasine land",
                "description": "Incomplete or paid. Gaps are shown; names are not invented.",
            },
        ],
        "tools": [
            {"id": "scenarios", "status": "live", "label": "LVT / AGR scenario calculators"},
            {"id": "api", "status": "live", "label": "Public assessment and layer API"},
            {"id": "downloads", "status": "partial", "label": "Open layer downloads via API"},
            {"id": "scotlis", "status": "live", "label": "Link through to ScotLIS"},
            {
                "id": "filters",
                "status": "partial",
                "label": "Filter by vacant land and value band",
            },
        ],
        "data_policy": {
            "portal_scraping": False,
            "owners_from_inspire": False,
            "purchase_prices_from_inspire": False,
            "open_layers_only": True,
            "gaps_visible": True,
        },
    }


def place_context(
    lat: float,
    lng: float,
    *,
    postcode: str | None = None,
    parcel: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Who-holds / what-status card for one place, with honest gaps."""
    parcel_feature = parcel if parcel is not None else lookup_parcel_geojson(lat, lng)
    parcel_props = (parcel_feature or {}).get("properties") or {}

    vdl = vdl_at_point(lat, lng)
    vacant = bool(vdl.get("intersects"))

    ownership_flags: list[str] = []
    if vacant:
        ownership_flags.append("vacant_or_derelict_survey")
    if parcel_feature:
        ownership_flags.append("registered_cadastre")
    else:
        ownership_flags.append("no_inspire_parcel")

    return {
        "lat": lat,
        "lng": lng,
        "vacant_or_derelict": vacant,
        "vdl": vdl,
        "parcel": {
            "found": parcel_feature is not None,
            "label": parcel_props.get("label"),
            "inspire_id": parcel_props.get("inspire_id") or parcel_props.get("national_reference"),
            "area_sqm": parcel_props.get("area_sqm"),
            "note": "INSPIRE parcel is an indicative registered extent, not a title sheet.",
        },
        "public_or_crown": {
            "status": "linked",
            "on_this_point": None,
            "note": "No OGL point query is wired yet. Use the national public-land map.",
            "map_url": PUBLIC_LAND_MAP,
            "crown_hub": CROWN_ESTATE_HUB,
        },
        "local_authority_holding": {
            "status": "gap",
            "on_this_point": None,
            "reason": "National LA ownership layer is not openly licensed for this portal.",
        },
        "common_good": {
            "status": "gap",
            "on_this_point": None,
            "reason": "No single open national Common Good spatial layer.",
        },
        "private_or_sasine": {
            "status": "gap",
            "note": "Private names and Sasine extents stay on ScotLIS / paid products.",
        },
        "flags": ownership_flags,
        "scotlis": scotlis_links(lat, lng, postcode),
        "filters": {
            "vacant": vacant,
            "public_private": "unknown",
            "value_band": None,
        },
    }
