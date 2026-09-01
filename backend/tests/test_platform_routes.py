from fastapi.testclient import TestClient

from api.platform_routes import router


def test_platform_router_exposes_open_layer_paths():
    paths = {route.path for route in router.routes}
    assert "/layers/open/vdl" in paths
    assert "/layers/open/public-land" in paths
    assert "/api/roll.json" in paths
    assert "/api/catalog.json" in paths
    assert "/api/public-land.json" in paths
    assert "/platform/place" in paths
    assert "/platform/gaps" in paths
    assert "/downloads" in paths


def test_platform_entry_wraps_core_app():
    from api.main_platform import app

    # FastAPI 0.137+ stores include_router() as a tree (_IncludedRouter has no
    # .path). OpenAPI is the version-stable view of mounted HTTP paths.
    paths = set(app.openapi()["paths"])
    assert "/layers/open/vdl" in paths
    assert "/layers/open/public-land" in paths
    assert "/api/roll.json" in paths
    assert "/api/catalog.json" in paths
    assert "/platform/gaps" in paths
    assert "/square" in paths
    assert "/layers/catalog" in paths


def test_platform_entry_serves_gaps_and_catalog():
    from api.main_platform import app

    client = TestClient(app)
    gaps = client.get("/platform/gaps")
    assert gaps.status_code == 200
    body = gaps.json()
    assert body["gaps"]
    live_ids = {layer["id"] for layer in body["live"]}
    gap_ids = {layer["id"] for layer in body["gaps"]}
    assert "public_crown" in live_ids
    assert "public_crown" not in gap_ids
    catalog = client.get("/layers/catalog")
    assert catalog.status_code == 200
    assert catalog.json()["version"] == 2
    assert catalog.json()["brief"] == "docs/PLATFORM.md"
