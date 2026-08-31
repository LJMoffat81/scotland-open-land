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
| Planning applications | Linked | Per-council portals | Official view pages where verified; no national drawable WMS |
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
| `/api/vdl.json` | SVDLS by owner class |
| `/api/vdl-councils.json` | Vacant hectares × illustrative full AGR |
| `/api/place.json?pc=KY7+5NE` | Place lookup: AGR, parcel, vacant, registers |
| `/api/registers.json` | Verified official Common Good / CAT / planning / land-map URLs |
| `/api/catalog.json` | Live / linked / gap register |

## Vacant and derelict land

- Definitive register: [SVDLS site register](https://www.gov.scot/publications/the-scottish-vacant-and-derelict-land-survey-site-register/)
- Map overlay and rolls query a public FeatureServer republish of that survey year
- Illustrative AGR on vacant hectares uses council-flat full residual per m². It is not a bill
- The 32-council AGR roll now carries `vacantHa` and `vacantFullAgrGbp`

## Official title

Always send users who need a title sheet to [ScotLIS](https://scotlis.ros.gov.uk/). This platform does not sell or reconstruct title.

## Still not ingested (when openly licensed)

1. National local-authority holdings as a drawable layer (Spatial Hub is not open)
2. A single national Common Good / CAT spatial file under OGL
3. Licensed sales for finer-than-council value grain
