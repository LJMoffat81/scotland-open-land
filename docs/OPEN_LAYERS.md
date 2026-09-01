# Open land layers

Product brief: [PLATFORM.md](PLATFORM.md).  
Licensing: [DATA_LICENSING.md](DATA_LICENSING.md).

This file is coverage, not the destination brief. The brief is not rewritten to match the build.

Only layers that can be legally published for free public use are drawn on the map. Everything else is a **visible gap** with a link to the official source. No portal scraping.

| Layer | Status | Licence | Notes |
|-------|--------|---------|-------|
| AGR / scenarios | Live | Research estimate | Council-flat HPI residual. Plot can scale to INSPIRE mapped extent. Not a rates bill |
| ROS INSPIRE parcels | Live | ROS INSPIRE WMS | Geometry only; no owners. ScotLIS for the title sheet |
| Council extents | Live | ROS open | AGR choropleth |
| SVDLS vacant & derelict | Live | OGL | Survey polygons; owner class ≠ title. National and per-council hectare rolls |
| Public / Crown Estate | Live overlay | SG 2024 FeatureServer | Five bodies only, non-exhaustive. Not local-authority land |
| Planning applications | Linked | Per-council + ePlanning | 27 of 32 have a verified official view page in `data/config/registers.yaml`. Five use national ePlanning (Glasgow, East Renfrewshire, Renfrewshire, South Ayrshire, Orkney). No national drawable WMS |
| CAT / council assets | Linked | Per-council pages | Spatial Hub amalgamated register still requires login |
| Common Good | Linked | Per-council registers | No single open national spatial file |
| Fife land map | Linked | Fife Council | This council’s own terrier. Not a national layer |
| LA ownership (Spatial Hub) | Gap | Not open | Not ingested |
| Private names / Sasine | Gap | Paid / incomplete | Use ScotLIS |
| What3Words 3×3 m | Gap | Licensed | Not published on the public map |

## Open API (live preview)

| Endpoint | Content |
|----------|--------|
| `/api/roll.json?scenario=full_agr` | 32-council AGR roll, with SVDLS vacant ha and illustrative residual |
| `/api/roll.csv?scenario=full_agr` | Same as CSV |
| `/api/public-land.json` | Hectares by the five published bodies |
| `/layers/open/public-land` | Viewport polygons of those five bodies (SG 2024 FeatureServer) |
| `/api/vdl.json` | SVDLS by owner class |
| `/api/vdl-councils.json` | Vacant hectares × illustrative full AGR |
| `/api/place.json?pc=KY7+5NE` | Place lookup: compact AGR, parcel, vacant, public/Crown, registers |
| `/api/registers.json` | National sources plus per-council planning URLs (27 verified; 5 national ePlanning) |
| `/api/catalog.json` | Live / linked / gap register |

## Vacant and derelict land

- Definitive register: [SVDLS site register](https://www.gov.scot/publications/the-scottish-vacant-and-derelict-land-survey-site-register/)
- Map overlay and rolls query a public FeatureServer republish of that survey year
- Illustrative AGR on vacant hectares uses council-flat full residual per m². It is not a bill
- The 32-council AGR roll now carries `vacantHa` and `vacantFullAgrGbp`
- Shareable map story: `/?story=vacant_land` paints the choropleth as that residual

## Public and Crown Estate land

- Official map: [Scottish Public and Crown Estate Land](https://www.arcgis.com/apps/dashboards/a10668ccd4784209bf22e3adcef6b897)
- Overlay queries the public 2024 FeatureServer in the current map view (largest holdings first, capped)
- Five bodies only: Forestry and Land Scotland, NatureScot, Scottish Crown Estate, Scottish Water, Crofting Agricultural Holdings
- Not local-authority land, not a title sheet, not exhaustive even for those bodies
- A click on the map reports whether the point intersects a published holding

## Official title

Always send users who need a title sheet to [ScotLIS](https://scotlis.ros.gov.uk/). This platform does not sell or reconstruct title.

## Still not ingested (when openly licensed)

1. National local-authority holdings as a drawable layer (Spatial Hub is not open)
2. A single national Common Good / CAT spatial file under OGL
3. Licensed sales for finer-than-council value grain
