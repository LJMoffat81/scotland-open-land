from layers.registers import load_registers, registers_for_council, registers_payload


def test_registers_file_has_32_councils():
    data = load_registers()
    councils = data["councils"]
    assert len(councils) == 32
    assert all(code.startswith("S12") for code in councils)


def test_edinburgh_has_council_planning_url():
    card = registers_for_council("S12000036")
    assert card is not None
    assert card["planning"]["scope"] == "council"
    assert "edinburgh.gov.uk" in card["planning"]["url"]


def test_aberdeenshire_and_north_lanarkshire_verified():
    ab = registers_for_council("S12000034")
    nl = registers_for_council("S12000050")
    assert ab is not None and ab["planning"]["scope"] == "council"
    assert "aberdeenshire.gov.uk" in ab["planning"]["url"]
    assert nl is not None and nl["planning"]["scope"] == "council"
    assert "northlanarkshire.gov.uk" in nl["planning"]["url"]


def test_unknown_council_falls_back_to_national_eplanning():
    card = registers_for_council("S12000005")
    assert card is not None
    assert card["planning"]["scope"] == "national"
    assert "eplanning.scot" in card["planning"]["url"]


def test_fife_has_council_only_land_map():
    card = registers_for_council("S12000047")
    assert card is not None
    assert card["land_map"]["url"].startswith("https://fife.maps.arcgis.com")
    glasgow = registers_for_council("S12000049")
    assert glasgow is not None
    assert glasgow.get("land_map") is None


def test_registers_payload_counts():
    body = registers_payload()
    assert body["ok"] is True
    assert body["council_count"] == 32
    assert body["council_specific_planning"] == 19
    assert body["national"]["scotlis"]["url"].startswith("https://scotlis.ros.gov.uk")
