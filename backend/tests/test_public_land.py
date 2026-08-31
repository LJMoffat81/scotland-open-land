from unittest.mock import MagicMock, patch

import httpx

from layers.public_land import query_bbox, query_point


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


def test_public_land_bbox_parses_geojson():
    payload = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-3.4, 57.2],
                            [-3.2, 57.2],
                            [-3.2, 57.35],
                            [-3.4, 57.35],
                            [-3.4, 57.2],
                        ]
                    ],
                },
                "properties": {
                    "Organisation": "Scottish Crown Estate",
                    "SiteName": "Glenlivet",
                    "Area_Ha": 23094.7,
                    "OBJECTID": 1,
                },
            }
        ],
    }
    with patch("layers.public_land._client", return_value=_mock_client(payload)):
        geo = query_bbox(57.15, -3.5, 57.4, -3.1)
    assert geo["type"] == "FeatureCollection"
    assert geo["meta"]["ok"] is True
    assert geo["meta"]["layer"] == "public_land"
    props = geo["features"][0]["properties"]
    assert props["organisation"] == "Scottish Crown Estate"
    assert props["site_name"] == "Glenlivet"
    assert props["layer"] == "public_land"


def test_public_land_bbox_soft_fails_on_http_error():
    with patch(
        "layers.public_land._client",
        return_value=_mock_client(error=httpx.ConnectError("offline")),
    ):
        geo = query_bbox(57.15, -3.5, 57.4, -3.1)
    assert geo["type"] == "FeatureCollection"
    assert geo["features"] == []
    assert geo["meta"]["ok"] is False


def test_public_land_point_no_holdings():
    with patch(
        "layers.public_land._client",
        return_value=_mock_client({"features": []}),
    ):
        hit = query_point(55.9533, -3.1883)
    assert hit["ok"] is True
    assert hit["intersects"] is False
    assert hit["holdings"] == []


def test_public_land_point_hit():
    payload = {
        "features": [
            {
                "attributes": {
                    "Organisation": "Forestry and Land Scotland",
                    "SiteName": None,
                    "Area_Ha": 420.3,
                    "OBJECTID": 12,
                }
            }
        ]
    }
    with patch("layers.public_land._client", return_value=_mock_client(payload)):
        hit = query_point(57.25, -3.3)
    assert hit["ok"] is True
    assert hit["intersects"] is True
    assert hit["holdings"][0]["organisation"] == "Forestry and Land Scotland"
    assert "not a legal title" in hit["note"].lower()
