# Albion Online Web Crawler

## Description
This Python script is designed to crawl specific URLs from the Albion Online Character Builder website and download all rendered images from the database. It saves them in folders based on build ID, with all armor-related images organized into their own folder, as well as separate folders for abilities. This tool is particularly useful for guilds that utilize a build template and prefer not to download each image manually.

You can enter multiple URLs in `url.txt`, and they will be processed sequentially, with each URL having its own designated folder. If you prefer not to enter URLs in the text file, you can leave it empty and input them directly in the console manually.

## Prerequisites
Before running the crawler, ensure you have the following installed:
- **Python 3.x**: Make sure Python is installed on your system.
- **ChromeDriver**: Download and install the ChromeDriver version that matches your Chrome browser. You can find it [here](https://sites.google.com/chromium.org/driver/downloads). Set the path in `config.txt`.

## Installation

1. **Download the files in this repo**
  
2. **Install Required Packages:**
     Use pip to install the necessary Python packages. You can install all dependencies listed in requirements.txt by running:

3. **Set Up Configuration:**
     Open the config.txt file and specify the path to your ChromeDriver.
     For example: CHROME_DRIVER_PATH=C:\path\to\your\chromedriver.exe

4. **Input URLs:**
     Edit the url.txt file and add the URLs you want to crawl, one per line.
   
     Example: https://albiononline.com/characterbuilder/solo-builds/view/3917
              https://albiononline.com/characterbuilder/solo-builds/view/3917

## Usage

1. **Open CMD and cd to the path you saved the tool in**
   Example : cd Desktop\Crawler

2. **To run the crawler, execute the following command in your terminal:**
    "python crawler.py"


