from api.platform_routes import router


def test_platform_router_exposes_open_layer_paths():
    paths = {route.path for route in router.routes}
    assert "/layers/open/vdl" in paths
    assert "/platform/place" in paths
    assert "/platform/gaps" in paths
    assert "/downloads" in paths


def test_platform_entry_wraps_core_app():
    from api.main_platform import app

    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/layers/open/vdl" in paths
    assert "/platform/gaps" in paths
    assert "/square" in paths
    assert "/layers/catalog" in paths
