Given the following mission parameters:
- Mission name: {mission_name}
- Satellite class: {satellite_class}
- Orbit: {orbit_altitude_km} km, {inclination_deg}° ({orbit_type})
- Payload: {payload_type}

Write a Risk Analysis section for a satellite feasibility study.

Cover:
1. Top 5–8 mission risks (technical, schedule, regulatory, operational)
2. For each risk: description, likelihood (1–5), impact (1–5), risk score (likelihood × impact), mitigation strategy
3. Risk matrix in Markdown table format: columns = Risk ID | Description | Likelihood | Impact | Score | Mitigation
4. One residual risk with no practical mitigation and how it is accepted/monitored

All risks must be specific to a {satellite_class} at {orbit_altitude_km} km performing {mission_application}.
Output in Markdown.
