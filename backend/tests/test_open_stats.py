from unittest.mock import patch

from layers.open_stats import public_land_json, roll_json, vdl_json


def test_public_land_json_maps_rows():
    rows = [
        {"Organisation": "Forestry and Land Scotland", "n": 10, "ha": 100.5},
        {"Organisation": "NatureScot", "n": 2, "ha": 20.0},
    ]
    with patch("layers.open_stats._stats", return_value=rows):
        body = public_land_json()
    assert body["ok"] is True
    assert body["totalHectares"] == 120.5
    assert body["bodies"][0]["organisation"] == "Forestry and Land Scotland"


def test_vdl_json_converts_sqm_to_hectares():
    rows = [{"owner_1": "Local Authority", "n": 3, "sqm": 20_000.0}]
    with patch("layers.open_stats._stats", return_value=rows):
        body = vdl_json()
    assert body["ok"] is True
    assert body["byOwnerClass"][0]["hectares"] == 2.0
    assert body["totalHectares"] == 2.0


def test_roll_json_joins_vacant_hectares():
    vacant = {"S12000036": {"vacantHa": 10.0, "vacantSites": 4}}
    geo = {
        "features": [
            {
                "properties": {
                    "code": "S12000036",
                    "name": "City of Edinburgh",
                    "site_rental_per_sqm_gbp": 20.0,
                }
            }
        ]
    }
    with (
        patch("layers.open_stats.by_council_hectares", return_value=vacant),
        patch("layers.open_stats.build_council_metrics_geojson", return_value=geo),
    ):
        body = roll_json("full_agr")
    row = body["councils"][0]
    assert row["vacantHa"] == 10.0
    assert row["vacantFullAgrGbp"] == 2_000_000.0
