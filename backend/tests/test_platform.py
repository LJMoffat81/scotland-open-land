from layers.platform import place_context, platform_catalog, scotlis_links


def test_platform_catalog_has_brief_layers():
    cat = platform_catalog()
    ids = {layer["id"] for layer in cat["layers"]}
    assert cat["version"] == 2
    assert cat["brief"] == "docs/PLATFORM.md"
    assert "agr_value" in ids
    assert "vdl" in ids
    assert "la_holdings" in ids
    assert "common_good" in ids
    assert cat["data_policy"]["portal_scraping"] is False
    assert cat["data_policy"]["gaps_visible"] is True
    statuses = {layer["id"]: layer["status"] for layer in cat["layers"]}
    assert statuses["vdl"] == "live"
    assert statuses["la_holdings"] == "gap"
    assert statuses["common_good"] == "gap"


def test_scotlis_links_point_to_official_service():
    links = scotlis_links(55.9533, -3.1883, postcode="EH1 1YZ")
    assert "scotlis.ros.gov.uk" in links["public_home"]
    assert "ros.gov.uk" in links["about"]
    assert links["search_hint"] == "EH1 1YZ"
    assert "title" in links["note"].lower()


def test_place_context_exposes_gaps():
    card = place_context(55.9533, -3.1883, postcode="EH1 1YZ")
    assert "vacant_or_derelict" in card
    assert card["local_authority_holding"]["status"] == "gap"
    assert card["common_good"]["status"] == "gap"
    assert card["private_or_sasine"]["status"] == "gap"
    assert "scotlis.ros.gov.uk" in card["scotlis"]["public_home"]
    assert card["filters"]["public_private"] == "unknown"
