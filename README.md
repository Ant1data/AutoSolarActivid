# AutoSolarActivid

**AutoSolarActivid** automatically generates daily and weekly videos illustrating solar activity by combining three public data sources:
1. SOHO LASCO C2 coronagraph images (NASA/ESA)
2. GOES proton flux (NOAA SWPC)
3. Neutron monitor flux (NMDB network)

The videos are stacked vertically (SOHO / Protons / Neutrons) using OpenCV and Matplotlib (plus Pillow). This project is an evolved fork of [SolarActivid](https://github.com/marcroussel/SolarActivid) with GitHub Actions automation.

## Features

* Automatic daily and weekly generation (cron + manual dispatch).
* Parallel download of SOHO images and creation of a 15s clip (60 FPS).
* Dynamic visualization of proton flux (energies >=10, >=50, >=100, >=500 MeV).
* Multi‑station neutron visualization (KERG, OULU, TERA) with Pearson correlation calculations.
* Vertical assembly of the three segments into a single MP4 video (mp4v codec).
* Localized weekly naming: `Week n°X (DDMMYYYY-DDMMYYYY).mp4` (currently still French in code as `Semaine`).
* Automatic cleanup of videos older than 14 days / configurable weekly retention limit.
* Migration workflow for legacy artifacts (`migrate_artifacts.yml`).

## Requirements

* Python 3.11 (GitHub Actions) – works locally >=3.9.
* Core libraries:
  * `requests`, `pandas`, `numpy`, `matplotlib`, `Pillow`
  * `opencv-python-headless`, `scipy`
  * (`jq` & `gh` provided in the Actions environment for the migration workflow)
* See `requirements.txt` for the full list.

## Installation

Clone the repository:

```bash
git clone https://github.com/Ant1data/AutoSolarActivid.git
cd AutoSolarActivid
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Daily generation (local)
```bash
python autovideo_daily.py
```
Produces a file:
```
solar_activity_videos/daily/<YYYY>/<Month>/DDMMYYYY_solar_activity.mp4
```

### Weekly generation (local)
```bash
python autovideo_weekly.py
```
Produces a file:
```
solar_activity_videos/weekly/<YYYY>/<Month>/Week n°X (DDMMYYYY-DDMMYYYY).mp4
```

### GitHub Actions
Two scheduled workflows:
* `solar_daily.yml` – runs every day at 00:00 UTC + manual dispatch.
* `solar_weekly.yml` – runs every Monday at 00:00 UTC + manual dispatch.
One ad‑hoc workflow:
* `migrate_artifacts.yml` – imports legacy MP4 artifacts into the new tree (`manual_import`).

To trigger manually: Actions tab > select workflow > "Run workflow".

## Project Structure

```
AutoSolarActivid/
  autovideo_daily.py
  autovideo_weekly.py
  requirements.txt
  solar_activity_videos/
    daily/<YYYY>/<Month>/DDMMYYYY_solar_activity.mp4
    weekly/<YYYY>/<Month>/Week n°X (DDMMYYYY-DDMMYYYY).mp4
  .github/workflows/
    solar_daily.yml
    solar_weekly.yml
    migrate_artifacts.yml
```

Temporary internal folders: `SOHO_videos/`, `SOHO_7days/`, `Protons_7days/`, `Neutrons_7days/`.

The historical folder `solar_activity/` is no longer used (replaced by direct downloads from official sources).

## Naming & Retention
* Video length: 15 seconds – 60 FPS (900 frames).
* Automatic purge > 14 days for daily and weekly.
* Weekly retention limit parameter (`MAX_WEEKLY_VIDEOS`).

## Data Sources & Credits
* SOHO LASCO C2 images – © NASA/ESA: https://soho.nascom.nasa.gov
* GOES Proton Flux – NOAA SWPC: https://services.swpc.noaa.gov
* NMDB Neutron Monitor Database: https://www.nmdb.eu

Thanks to the providers of public data. Attribution overlays appear on each video segment.

## Contributing

Contributions welcome: performance optimizations (e.g., frame interpolation), adding new neutron stations, caption internationalization.
1. Fork
2. Branch (`git checkout -b feature/my-feature`)
3. Commit (`git commit -m 'Add: my feature'`)
4. Push (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
