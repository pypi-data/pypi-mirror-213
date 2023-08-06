# ve-power-meter

Power measurement tool for NEC Vector Engine

## Installation

```
pip install ve-power-meter
```

## Usage

```
$ ve-power-meter
timestamp,power.draw,temperature.core,temperature.memory
2023/06/13 12:15:10.275,47.04,45,40
2023/06/13 12:15:11.292,47.04,45,40
2023/06/13 12:15:12.309,47.01,45,40
2023/06/13 12:15:13.326,47.01,47,44
2023/06/13 12:15:14.342,145.38,49,50
2023/06/13 12:15:15.358,173.39,50,50
2023/06/13 12:15:16.373,173.39,51,52
2023/06/13 12:15:17.390,170.48,51,53
2023/06/13 12:15:18.405,170.48,51,54
2023/06/13 12:15:19.421,177.39,52,54
```

### Notes:

- `vecmd` must be available at `/opt/nec/ve/mmm/bin/vecmd` (tested with mmm v1.3.78).
- Metrics are printed out every second.
- `temperature.core` is the average temperature of all cores (Celsius).
- `temperature.memory` is the average temperature of all HBM modules (Celsius).
- `power.draw` is `AUX 12V V * AUX 12V C + Edge 12V V * Edge 12V C` (Watts).
