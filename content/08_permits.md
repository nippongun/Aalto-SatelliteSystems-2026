<!-- ai-draft: 2026-04-19, awaiting student review -->

# Permits and Regulatory Compliance

## Satellite Operation Authorisation (Finland)

AtmoSat-1 requires authorisation for space activities under Finnish law. The Act on Space Activities (Finland) entered into force on 23 January 2018, supplemented by the Decree of the Ministry of Economic Affairs and Employment on Space Activities.

Every Finnish satellite requires:

- **Authorisation for space activities** granted by the Ministry of Economic Affairs and Employment
- The authorisation covers the entire mission lifecycle: launch, in-orbit operations, and disposal

Reference: https://tem.fi/en/spacelaw

## Radio Frequency Licence

In Finland, radio frequency coordination is handled by FICORA (Finnish Communications Regulatory Authority, Viestintävirasto). The licensing process depends on the frequency band used:

For amateur radio bands (UHF 430–440 MHz, common for CubeSats):
- Radio amateur licence applied from the national Radio Amateur Organization (SRAL in Finland)
- The Radio Amateur Organization coordinates the licence with the International Telecommunication Union (ITU) via the International Amateur Radio Union (IARU)

For commercial frequency bands (S-band, X-band):
- Frequency coordination applied directly through FICORA
- ITU coordination required for interference protection

AtmoSat-1 frequency band selection is pending (see mission_config.yaml). Frequency selection drives the licence pathway. Note: X-band downlink requires commercial frequency coordination; UHF amateur band has a simpler licence process but limits downlink data rate significantly.

## Satellite Disposal

AtmoSat-1 shall comply with ESA space debris mitigation guidelines. At the operational altitude of 500 km SSO, atmospheric drag produces natural orbital decay in approximately 7–12 years (solar cycle dependent), satisfying the 25-year passive re-entry rule without active propulsion or a drag sail.

## Launch Provider Requirements

The satellite shall satisfy all launch provider regulatory requirements before integration, including:

- Vibration test report (required by every launch provider)
- Thermal vacuum test compliance documentation
- EMC test compliance
- Radiation tolerance assessment for the target orbit environment (~500 km SSO)

## Export Control

Components sourced from the United States may be subject to US Export Administration Regulations (EAR) or International Traffic in Arms Regulations (ITAR). A review of all COTS components shall be conducted before procurement to identify any export-controlled items.
