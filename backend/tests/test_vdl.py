from unittest.mock import MagicMock, patch

import httpx

from layers.vdl import query_bbox, query_point


def _mock_client(payload=None, error: Exception | None = None) -> MagicMock:
    client = MagicMock()
    client.__enter__.return_value = client
    client.__exit__.return_value = False
    if error is not None:
        client.get.side_effect = error
        return client
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = payload
    client.get.return_value = response
    return client


def test_vdl_bbox_parses_geojson():
    payload = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-4.3, 55.85],
                            [-4.2, 55.85],
                            [-4.2, 55.86],
                            [-4.3, 55.86],
                            [-4.3, 55.85],
                        ]
                    ],
                },
                "properties": {
                    "site_name": "Test vacant site",
                    "site_type": "Vacant",
                    "site_size": 1.2,
                    "local_auth": "Glasgow City",
                    "owner_1": "Local authority",
                    "site_code": "G123",
                },
            }
        ],
    }
    with patch("layers.vdl._client", return_value=_mock_client(payload)):
        geo = query_bbox(55.84, -4.35, 55.87, -4.15)
    assert geo["type"] == "FeatureCollection"
    assert geo["meta"]["ok"] is True
    assert geo["meta"]["layer"] == "vdl"
    assert geo["features"][0]["properties"]["name"] == "Test vacant site"
    assert geo["features"][0]["properties"]["layer"] == "vdl"


def test_vdl_bbox_soft_fails_on_http_error():
    with patch(
        "layers.vdl._client",
        return_value=_mock_client(error=httpx.ConnectError("offline")),
    ):
        geo = query_bbox(55.84, -4.35, 55.87, -4.15)
    assert geo["type"] == "FeatureCollection"
    assert geo["features"] == []
    assert geo["meta"]["ok"] is False


def test_vdl_point_no_sites():
    with patch(
        "layers.vdl._client",
        return_value=_mock_client({"features": []}),
    ):
        hit = query_point(55.9533, -3.1883)
    assert hit["ok"] is True
    assert hit["intersects"] is False
    assert hit["sites"] == []
