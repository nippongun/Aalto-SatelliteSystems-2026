Given the following mission parameters:
- Mission name: {mission_name}
- Satellite class: {satellite_class}
- Orbit: {orbit_altitude_km} km, {inclination_deg}° ({orbit_type})
- Payload: {payload_type}
- Ground station: {ground_station}
- Downlink frequency: {frequency_GHz} GHz

Write the "Operations Concept" subsection of the Mission Design chapter.

Cover:
1. Mission phases: launch, LEOP, commissioning, nominal operations, decommissioning
2. Nominal operations loop: data collection cadence, on-board storage, downlink window
3. Ground contact geometry: passes per day over {ground_station}, average contact duration at {orbit_altitude_km} km
4. Data flow: payload → on-board storage → downlink → ground processing → data product delivery

Output in Markdown. Use ## for subsections. Include a simple ASCII timeline or bullet sequence for the nominal operations loop.
