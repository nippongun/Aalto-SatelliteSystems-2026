# Payload Selection

AtmoSat-1 carries two spectrometer channels: a UV channel for ozone DOAS retrieval (OBS-01/02) and a SWIR channel for combustion anomaly detection via multi-temporal radiance comparison (OBS-03/04). Both must fit within the 3U envelope alongside the bus, with combined payload mass and power consistent with REQ-07 and REQ-09.

## UV Channel Trade-off (270–340 nm, ≤ 1 nm FWHM)

The UV channel must resolve the Hartley–Huggins ozone absorption band structure to enable DOAS retrieval (OBS-01). Four options were assessed.

| Criterion            | **A: Ocean Insight STS-UV** (grating) | **B: Avantes AvaSpec-Mini** (grating) | **C: Hamamatsu C13555MA** (grating array) | **D: Filter wheel + photodiode** |
|----------------------|--------------------------------------|--------------------------------------|------------------------------------------|----------------------------------|
| Mass                 | ~45 g | ~200 g | ~80 g | ~15 g |
| Power                | ~0.45 W | ~0.7 W | ~0.5 W | ~0.1 W |
| FWHM                 | ~1.5 nm | ~0.3–0.8 nm | ~1.5 nm | N/A (no spectrum) |
| OBS-01 met?          | Yes | Yes | Yes | No |
| DOAS-capable?        | Yes | Yes | Yes | No |
| 3U fit?              | Yes | Yes | Yes | Yes |
| Heritage             | High | Medium | Medium | High |
| Cost                 | Low | Medium | Low-Medium | Very low |

**Option D** (filter wheel) cannot produce continuous spectra and therefore cannot support DOAS retrieval; it is eliminated.

**Option B** (Avantes AvaSpec-Mini) meets the spectral requirement but at 200 g it leaves insufficient mass margin for the SWIR instrument (~40 g), structural mounting, and baffling within the 1U payload volume. Eliminated on mass.

**Selected: Option A (Ocean Insight STS-UV)**. Mass ~45 g, power ~0.45 W, FWHM ~1.5 nm, extensive CubeSat heritage.

**Space qualification risk:** The STS-UV is a commercial lab instrument. A space-qualified variant with radiation-hardened UV detector, hermetic sealing, and thermal stability is required for flight. Baseline fallback: if the commercial unit fails space qualification, replace with a space-qualified UV spectrometer of equivalent spectral performance (e.g., Ibsen Photonics FREEDOM UV series with radiation-tolerant detector). The DOAS retrieval is hardware-agnostic; only spectral range and FWHM are binding constraints on the replacement. Final qualification verification is a PDR activity.

## SWIR Anomaly Channel Trade-off (2.28–2.34 µm, ≤ 15 nm FWHM)

The SWIR channel is designed for **qualitative anomaly detection**, not quantitative CO column retrieval. At 10–15 nm FWHM, CO lines cannot be resolved and H₂O interference cannot be separated — quantitative CO retrieval would require resolving power ~23,000 (0.1 nm FWHM), physically unachievable in a 3U form factor. The channel instead detects **relative radiance anomalies** against a multi-temporal regional baseline: a statistically significant drop in 2.3 µm band radiance, correlated in time and location with other event indicators (ozone anomaly, fire radiative power products), constitutes a combustion event flag. The ≤ 15 nm FWHM requirement enables MEMS Fabry-Pérot instruments.

| Criterion            | **A: Spectral Engines NIRONE S2.2** (MEMS-FP) | **B: Hamamatsu C14384 InGaAs array** | **C: Si-Ware NeoSpectra** (MEMS-FP) | **D: Narrowband filter (2.31 µm) + InGaAs diode** |
|----------------------|----------------------------------------------|--------------------------------------|-------------------------------------|---------------------------------------------------|
| Mass                 | ~40 g | ~400 g | ~20 g | ~10 g |
| Power                | ~0.5 W | ~2.0 W | ~0.8 W | ~0.1 W |
| Spectral range       | 2.0–2.5 µm | 0.9–2.5 µm | 1.35–2.5 µm | 2.31 µm only (±5 nm) |
| FWHM                 | ~10–15 nm | ~2 nm | ~16 nm | N/A (single channel) |
| OBS-03 met?          | Yes | Yes | No (16 nm) | N/A |
| Anomaly detection?   | Yes | Yes | Yes | Yes (simplified) |
| 3U fit?              | Yes | No (mass/power) | Yes | Yes |
| Heritage             | Low-Medium | Low | Low-Medium | High |

**Option B** (Hamamatsu InGaAs array) clearly exceeds FWHM requirements and covers the full range, but at 400 g and 2.0 W it is incompatible with a 3U platform alongside a UV channel and bus systems.

**Option C** (Si-Ware NeoSpectra) at ~16 nm FWHM does not meet the ≤ 15 nm requirement; eliminated.

**Option D** (single narrowband filter + InGaAs photodiode) provides a single radiance point at 2.31 µm. While adequate for total-column band-depth at a known CO wavelength, it offers no spectral context to normalise against continuum or separate CO from H₂O absorption. Rejected due to insufficient retrieval robustness.

**Selected: Option A (Spectral Engines NIRONE S2.2)**. Mass ~40 g, power ~0.5 W, FWHM ~10–15 nm. Meets OBS-03 (≤ 15 nm). Detection via multi-temporal relative radiance change, not CO line retrieval. Radiometric repeatability and thermal stability are the critical performance parameters; to be verified at PDR.

## Selected Payload Summary

| Item | Value |
|------|-------|
| UV channel | Ocean Insight STS-UV (grating spectrometer) |
| SWIR channel | Spectral Engines NIRONE S2.2 (MEMS Fabry-Pérot) |
| Combined mass (instruments) | ~85 g |
| Combined peak power | ~0.95 W |
| Peak data rate (UV + SWIR) | ~0.5 Mbps (USB, burst during overpass) |
| 3U envelope compatibility | Yes — both instruments fit within 1U payload volume (~100 cm³) |

Combined instrument mass and power are well within the REQ-07 (≤ 4 kg) envelope. Power, link, and mass budgets (including OBC, ADCS, comms, structure) will be completed at Preliminary Design.

**Swath architecture: cross-track scanning mirror.** The STS-UV and NIRONE S2.2 are slit spectrometers producing a single spatial sample per integration. A 1-axis cross-track scan mirror mounted before the instrument slit provides spatial coverage. At 500 km altitude, a ±8.5° half-angle scan produces a 150 km swath (2 × 500 × tan 8.5° ≈ 150 km). Step-and-stare operation is synchronized with detector integration time. Scanning mirror mechanisms are a well-established CubeSat technique; mass and power impact will be budgeted at PDR.

**SNR targets:** OBS-02 (UV SNR ≥ 100) and OBS-04 (SWIR SNR ≥ 200) are preliminary targets derived from comparable small-satellite atmospheric missions and will be validated through radiometric modelling (aperture, integration time, detector quantum efficiency, optical throughput, noise model) at PDR.
