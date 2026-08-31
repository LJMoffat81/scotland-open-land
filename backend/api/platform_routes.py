"""Open land platform HTTP routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from layers.platform import place_context, platform_catalog
from layers.public_land import query_bbox as public_land_bbox
from layers.vdl import query_bbox as vdl_bbox

router = APIRouter()


def _scotland_bounds_check(lat: float, lng: float) -> None:
    if lat < 54.5 or lat > 61.0 or lng < -8.5 or lng > -0.5:
        raise HTTPException(status_code=400, detail="Coordinates appear to be outside Scotland.")


@router.get("/layers/open/vdl")
def layer_open_vdl(
    south: float = Query(..., description="BBox south latitude"),
    west: float = Query(..., description="BBox west longitude"),
    north: float = Query(..., description="BBox north latitude"),
    east: float = Query(..., description="BBox east longitude"),
    max_features: int = Query(default=80, ge=1, le=80),
) -> JSONResponse:
    """Vacant and derelict land polygons in the viewport (OGL survey overlay)."""
    _scotland_bounds_check((south + north) / 2.0, (west + east) / 2.0)
    return JSONResponse(vdl_bbox(south, west, north, east, max_features=max_features))


@router.get("/layers/open/public-land")
def layer_open_public_land(
    south: float = Query(..., description="BBox south latitude"),
    west: float = Query(..., description="BBox west longitude"),
    north: float = Query(..., description="BBox north latitude"),
    east: float = Query(..., description="BBox east longitude"),
    max_features: int = Query(default=80, ge=1, le=80),
) -> JSONResponse:
    """Public and Crown Estate holdings in the viewport (SG 2024 overlay)."""
    _scotland_bounds_check((south + north) / 2.0, (west + east) / 2.0)
    return JSONResponse(
        public_land_bbox(south, west, north, east, max_features=max_features)
    )


@router.get("/platform/place")
def platform_place(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    postcode: str | None = Query(default=None),
) -> dict:
    """Ownership / vacant / gap card for one point."""
    _scotland_bounds_check(lat, lng)
    return place_context(lat, lng, postcode=postcode)


@router.get("/platform/gaps")
def platform_gaps() -> dict:
    """Visible register gaps — first-class product, not hidden."""
    catalog = platform_catalog()
    return {
        "brief": catalog["brief"],
        "gaps": [layer for layer in catalog["layers"] if layer["status"] in ("gap", "linked")],
        "live": [layer for layer in catalog["layers"] if layer["status"] == "live"],
        "policy": catalog["data_policy"],
    }


@router.get("/downloads")
def open_downloads() -> dict:
    """Index of freely licensed layers and official sources."""
    return {
        "note": (
            "Only openly licensed material is offered here. "
            "Spatial Hub login layers are listed as sources, not mirrored."
        ),
        "items": [
            {
                "id": "vdl_register",
                "label": "SVDLS site register",
                "licence": "OGL-3.0",
                "url": "https://www.gov.scot/publications/the-scottish-vacant-and-derelict-land-survey-site-register/",
            },
            {
                "id": "vdl_overlay",
                "label": "VDL map overlay (this API)",
                "licence": "OGL-3.0",
                "endpoint": "/layers/open/vdl",
            },
            {
                "id": "public_land_overlay",
                "label": "Public / Crown land overlay (this API)",
                "licence": "SG 2024 dashboard overlay — not a title",
                "endpoint": "/layers/open/public-land",
                "note": "Viewport query of the official map. Five bodies only.",
            },
            {
                "id": "council_agr",
                "label": "Council AGR metrics GeoJSON",
                "licence": "research estimate + OGL inputs",
                "endpoint": "/layers/councils",
            },
            {
                "id": "inspire_parcels",
                "label": "ROS INSPIRE cadastral parcels",
                "licence": "ROS INSPIRE / Crown",
                "url": "https://www.ros.gov.uk/open-data",
            },
            {
                "id": "public_crown_map",
                "label": "Scottish public and Crown Estate land map",
                "licence": "official SG map — link, not a copy",
                "url": "https://www.arcgis.com/apps/dashboards/a10668ccd4784209bf22e3adcef6b897",
            },
            {
                "id": "scotlis",
                "label": "ScotLIS official titles",
                "licence": "ROS service",
                "url": "https://scotlis.ros.gov.uk/",
            },
        ],
    }
