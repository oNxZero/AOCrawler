# Albion Online Web Crawler

Download images from Albion Online Character Builder pages. Output is grouped by build ID, with separate folders for equipment and abilities.

## Setup

Install Python, Chrome, and a ChromeDriver version matching your browser. Then install the Python dependencies:

```bash
pip install -r requirements.txt
```

Set the driver and output paths in `config.txt`:

```text
CHROME_DRIVER_PATH=C:\path\to\chromedriver.exe
OUTPUT_FOLDER_PATH=C:\path\to\output
```

## Run

Put one build URL per line in `url.txt`, for example:

```text
https://albiononline.com/characterbuilder/solo-builds/view/3917
```

Run from the project directory:

```bash
python crawler.py
```

URLs are processed in order. Leave `url.txt` empty to enter them in the console instead.
