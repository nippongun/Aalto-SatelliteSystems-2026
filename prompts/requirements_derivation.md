Given the following mission parameters:
- Mission name: {mission_name}
- Satellite class: {satellite_class}
- Mission application: {mission_application}
- Payload: {payload_type}
- Orbit: {orbit_altitude_km} km, {inclination_deg}°

Derive the requirements for the "Requirements Analysis" section of a satellite feasibility study.

Produce:
1. Mission objectives (3–5, each with a measurable success criterion)
2. For each objective: 2–4 system requirements in the form "The satellite shall [verb] [parameter] [≥/≤/=] [value] [unit]"
3. A traceability summary: which requirements trace to which objective

Use the YAML format below for each requirement (to be added to requirements/requirements.yaml):
```yaml
objectives:
  - id: OBJ-01
    text: "[objective text]"
    requirements:
      - id: REQ-01
        text: "The satellite shall [...]"
```

Output the YAML block first, then a plain-English narrative explaining the rationale for each objective.
Write at the level of an Aalto MSc satellite systems feasibility study.
