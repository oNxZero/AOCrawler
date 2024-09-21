# Albion Online Web Crawler

## Description
This Python script is designed to **crawl specific URLs** from the Albion Online Character Builder website and download all rendered images from the database. It organizes these images into folders based on **build ID**, with separate folders for **armor-related images** and **abilities**. 

This tool is particularly beneficial for guilds that utilize build templates and prefer not to download each image manually.

You can enter multiple URLs in `url.txt`, and they will be processed sequentially, with each URL having its own designated folder. If you prefer not to enter URLs in the text file, you can leave it empty and input them directly in the console.

## Prerequisites
Before running the crawler, ensure you have the following installed:
- **Python 3.x**: Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **ChromeDriver**: Download and install the ChromeDriver version that matches your Chrome browser. You can find it [here](https://sites.google.com/chromium.org/driver/downloads). Once downloaded, set the path in `config.txt`.

## Installation

1. **Download the files in this repo**
  
2. **Install Required Packages:**
     Use pip to install the necessary Python packages. You can install all dependencies listed in requirements.txt by running:
   ```bash
     pip install -r requirements.txt

4. **Set Up Configuration:**
     Open the config.txt file and specify the path to your ChromeDriver.
   ```bash
     CHROME_DRIVER_PATH=C:\path\to\your\chromedriver.exe
     OUTPUT_FOLDER_PATH=\path\to\your\desired folder

5. **Input URLs:**
     Edit the url.txt file and add the URLs you want to crawl, one per line.
   ```bash
     Example: https://albiononline.com/characterbuilder/solo-builds/view/3917
              https://albiononline.com/characterbuilder/solo-builds/view/3917

## Usage

1. **Open CMD and cd to the path you saved the tool in**
    ```bash
   cd Desktop\Crawler

3. **To run the crawler, execute the following command in your terminal:**
     ```bash
    python crawler.py

4. **wait for the program to finish and enjoy your crawled images :)**


