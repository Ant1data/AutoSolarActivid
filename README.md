# AutoSolarActivid

**AutoSolarActivid** is a Python-based tool designed to automatically generate daily and weekly videos illustrating solar activity. It reads solar data from CSV files and creates videos using the `moviepy` library. This project is a fork of [SolarActivid](https://github.com/marcroussel/SolarActivid).

## Features

* **Automated video generation**: Create daily and weekly videos from solar activity data.
* **CSV data processing**: Read and process CSV files containing solar measurements.
* **Video creation with MoviePy**: Assemble videos programmatically using `moviepy`.

## Requirements

* Python 3.6 or higher
* Python libraries:

  * `moviepy`
  * `pandas`
  * Other dependencies listed in `requirements.txt`

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

### Daily Video Generation

To generate a daily video:

```bash
python autovideo_daily.py
```

### Weekly Video Generation

To generate a weekly video:

```bash
python autovideo_weekly.py
```

## Project Structure

* `autovideo_daily.py` : Script to generate daily videos.
* `autovideo_weekly.py` : Script to generate weekly videos.
* `requirements.txt` : Python dependencies.
* `solar_activity/` : Folder containing CSV files with solar activity data.

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push your branch (`git push origin feature/my-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
