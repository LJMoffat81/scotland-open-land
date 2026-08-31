# Open land layers

Product brief: [PLATFORM.md](PLATFORM.md).  
Licensing: [DATA_LICENSING.md](DATA_LICENSING.md).

Only layers that can be legally published for free public use are drawn on the map. Everything else is a **visible gap** with a link to the official source.

| Layer | Status | Licence | Notes |
|-------|--------|---------|-------|
| AGR / scenarios | Live | Research estimate | Residual engine — not a rates bill |
| ROS INSPIRE parcels | Live | ROS INSPIRE WMS | Geometry only; no owners |
| SVDLS vacant & derelict | Live overlay | OGL | Survey polygons; owner class ≠ title |
| Public / Crown Estate map | Linked | SG dashboard | National map of selected public bodies |
| LA ownership (Spatial Hub) | Gap | Not open (PSGA / other) | Not ingested |
| Council asset / CAT | Gap | Spatial Hub login | Not scraped |
| Common Good | Gap | Per-council registers | No single open national spatial file |
| Private names / Sasine | Gap | Paid / incomplete | Use ScotLIS |

## Vacant and derelict land

- Definitive register: [SVDLS site register](https://www.gov.scot/publications/the-scottish-vacant-and-derelict-land-survey-site-register/)
- Spatial Hub dataset: [Vacant and Derelict Land – Scotland](https://data.spatialhub.scot/dataset/vacant_and_derelict_land-is)
- Map overlay queries a public FeatureServer republish of that survey year

## Official title

Always send users who need a title sheet to [ScotLIS](https://scotlis.ros.gov.uk/). This platform does not sell or reconstruct title.

## Next ingest (when openly licensed)

1. OGL extract of public-body / Crown Estate Scotland holdings
2. Per-council Common Good and CAT tables that are published under OGL
3. National statistics and coverage indicators (registered vs Sasine, public vs unknown)
