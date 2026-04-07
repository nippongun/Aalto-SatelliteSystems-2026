<!-- ai-draft: 2026-03-23, awaiting student review -->

# Mission Motivation and Objectives

## Problem to be Solved

Armed conflict causes documented but poorly quantified damage to atmospheric chemistry. Industrial fires, munitions detonations, and the destruction of chemical plants release carbon monoxide (CO) and ozone-depleting substances in quantities that exceed normal anthropogenic baselines. The 2022–present conflict in Ukraine constitutes the largest such event in Europe in decades, yet continuous, spatially resolved atmospheric monitoring over the affected region is severely limited by the collapse of ground-based observation networks in conflict zones.

European resilience requires independent, space-based situational awareness of environmental threats that do not respect national borders. Ozone column depletion above conflict regions can affect UV exposure and agricultural productivity across neighbouring countries. Elevated CO concentrations are tracers of large-scale combustion events and serve as a proxy for both immediate health hazards and long-term ozone chemistry perturbations.

No existing European small satellite mission is dedicated to the joint monitoring of ozone and CO with the spatial and temporal resolution needed to attribute atmospheric changes to localised conflict activity. AtmoSat-1 addresses this gap.

## Why a Space-Based Solution is Needed

Ground-based atmospheric monitoring stations provide high accuracy but poor spatial coverage; they require continuous power, maintenance, and personnel — all unavailable in active conflict zones. Airborne platforms cannot safely operate over contested airspace. Only a satellite provides unimpeded, repeatable, overhead access to denied regions.

A Sun-Synchronous Orbit (SSO) at 750 km altitude with a 98.0° inclination provides daily revisit over all European latitudes. The fixed local solar time of an SSO eliminates diurnal solar angle variation as a confound, enabling direct comparison of UV-derived ozone column retrievals between overflights of different regions (e.g., Kyiv vs. Helsinki) without solar-geometry correction factors.

Existing large atmospheric monitoring missions (Sentinel-5P, TROPOMI) provide global coverage at 3.5 km × 5.5 km ground resolution but are not targeted instruments — AtmoSat-1 demonstrates that a 3U CubeSat can deliver targeted regional monitoring at lower cost and shorter development timeline, validating the small-satellite approach for future constellation deployments.

## Mission Goal

AtmoSat-1 shall measure the total ozone column and near-surface CO volume mixing ratio over selected European regions with sufficient accuracy and revisit frequency to detect conflict-attributable anomalies above natural variability.

Quantified goal: detect an ozone column change of ≥ 5 Dobson Units (DU) and a CO mixing ratio anomaly of ≥ 50 ppb relative to a seasonal baseline, over a ground swath of at least 200 km width, with a revisit period of ≤ 5 days at European mid-latitudes (45–70° N).

## Product of the Mission

The primary data products are:

### Level 1B: Calibrated Radiance Spectra

Calibrated top-of-atmosphere radiance spectra from the UV channel (270–340 nm, resolution ≤ 1 nm) and SWIR channel (2.3 µm CO absorption band, resolution ≤ 0.1 nm), geolocated to ≤ 2 km ground resolution at nadir.

### Level 2: Retrieved Geophysical Products

Total ozone column in Dobson Units derived from UV backscatter using the DOAS (Differential Optical Absorption Spectroscopy) retrieval algorithm, and CO total column in mol/m² derived from SWIR spectral fitting. Uncertainty targets: ozone ≤ 5 DU (1σ), CO ≤ 10% (1σ).

### Level 3: Regional Time Series

Gridded weekly composites at 0.25° × 0.25° spatial resolution over the European domain (30–75° N, 10° W–50° E), distributed as open-access NetCDF files via Aalto University repository infrastructure.

## Success Criteria

### Minimal Success

AtmoSat-1 survives launch, achieves operational orbit, and returns calibrated UV or SWIR radiance spectra for at least one overpass of a target region. Demonstrates viability of the CubeSat platform for atmospheric remote sensing. At least 10 days of science data acquired.

### Full Success

Both UV and SWIR channels operate nominally. Total ozone column and CO retrievals meet accuracy targets (ozone ≤ 5 DU, CO ≤ 10%). Minimum 90-day science mission. At least one statistically significant ozone or CO anomaly detected and attributed to a known anthropogenic source (conflict or industrial event) above the 3σ natural variability threshold. Data archived and publicly released.

### Extended Success

Mission lifetime exceeds 1 year. A multi-season dataset is produced enabling characterisation of conflict-driven atmospheric trends at European scale. Results published in a peer-reviewed journal or submitted as a course research report. Secondary albedo product from the visible/NIR camera channel is validated.

## Target Orbit Justification

### Altitude: 750 km

An altitude of 750 km is standard for ozone monitoring satellites. At 750 km:

- Ground swath width for a ±30° off-nadir FOV is approximately 870 km, enabling wide-area coverage per pass.
- Orbital period is approximately 99.9 minutes, giving ≈ 14.4 revolutions per day.
- Atmospheric drag is low enough for a mission lifetime exceeding 5 years without propulsion, simplifying the CubeSat bus.
- The Van Allen belt inner edge is at ~1000 km; 750 km keeps radiation dose below 5 krad/year for a 3U CubeSat with 2 mm aluminium shielding, within standard commercial component tolerance.

### Inclination: 98.0° (Sun-Synchronous)

An SSO at 750 km altitude requires an inclination of approximately 98.0° (retrograde). This provides:

- Constant local solar time (~10:30 descending node, matching Sentinel-5P for cross-calibration opportunity) eliminating diurnal variation as a confounding factor.
- Complete latitude coverage from 82° S to 82° N, encompassing all European conflict and reference sites.
- Repeatable solar illumination geometry, critical for UV reflectance retrievals where solar angle directly affects the depth of the ozone absorption feature.

## Scientific Objectives

SO-1: Quantify the total ozone column above conflict-affected regions of Eastern Europe with ≤ 5 DU accuracy on a weekly revisit basis.

SO-2: Measure CO total column above conflict-affected regions with ≤ 10% accuracy to characterise large-scale combustion events attributable to military activity.

SO-3: Compare ozone and CO anomalies over conflict regions (Ukraine, 46–52° N) against reference regions with similar meteorology but no active conflict (Finland, 60–70° N) to isolate conflict-driven signals from natural variability.

SO-4: Demonstrate that a 3U CubeSat UV + SWIR spectrometer suite can produce geophysical retrievals consistent with Sentinel-5P Level 2 products to within 10%, validating the small-satellite approach for future atmospheric monitoring constellations.

## Scientific Requirements

SR-1: The UV spectrometer shall cover 270–340 nm with a spectral resolution ≤ 1 nm full-width at half-maximum (FWHM) to resolve the Hartley–Huggins ozone absorption bands.

SR-2: The SWIR spectrometer shall cover the 2.28–2.34 µm CO absorption band with a spectral resolution ≤ 0.1 nm FWHM.

SR-3: Signal-to-noise ratio (SNR) shall be ≥ 100 in the UV channel at 305 nm for a 100% reflective Lambertian surface under nominal solar illumination at 750 km altitude.

SR-4: SNR shall be ≥ 200 in the SWIR channel at 2.31 µm under the same conditions.

SR-5: Geolocation accuracy shall be ≤ 2 km (1σ) at nadir.

SR-6: Radiometric calibration accuracy shall be ≤ 3% absolute.

## Observation Requirements

OR-1: Ground pixel size at nadir shall be ≤ 10 km × 10 km to allow attribution of CO anomalies to localised industrial or conflict sources.

OR-2: Swath width shall be ≥ 200 km to ensure coverage of the target region within a single overpass.

OR-3: Revisit period at 50° N shall be ≤ 5 days (1 day desirable with ground-track repeat or cross-track pointing).

OR-4: The instrument shall operate continuously during each sunlit pass of at least 90 s duration above the primary target region (45–70° N).

OR-5: Data acquired shall be downlinked to ground within 24 hours of acquisition.

## Mission Requirements

MR-1: The satellite platform shall comply with the 3U CubeSat standard (10 cm × 10 cm × 30 cm, mass ≤ 4 kg).

MR-2: The mission shall achieve a minimum operational lifetime of 90 days after commissioning.

MR-3: The payload shall receive ≥ 3 W average electrical power during sunlit observation phases.

MR-4: The satellite shall be compatible with a rideshare launch to an SSO at 750 km altitude (±50 km acceptable).

MR-5: All science data shall be stored on-board for a minimum of 24 hours pending downlink.

MR-6: The spacecraft attitude control system shall maintain nadir-pointing to within ±1° (3σ) during science observation.

MR-7: The satellite shall comply with ESA debris mitigation guidelines: orbital lifetime after end of mission shall not exceed 25 years, achievable passively at 750 km altitude.
