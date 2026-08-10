# Tracedate

Tracedate aims to helps the user rename their media files based on their creation date. A media file is defined here as essentially any digital file that contains a photo or a video. The timestamp is extracted from the file, either from the EXIF metadata or the filename, and the media file is renamed based on it. Say goodbye to cryptic names and organize camera and mic files in chronological order.

## Running the script with Docker

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/) installed on your machine.

### Steps
1. **Build the image:**
   Open your terminal in the root directory of this project and run:
   ```bash
   docker build -t tracedate .
   ```

2. **Run the container:**
   ```bash
   docker run --rm -it -v <target_directory_path>:/data tracedate -d /data

## Running the script locally with Python

### Prerequisites
- [Python](https://www.python.org/) (version 3.8 or higher recommended, tested with 3.11)
   
### Steps
1. **Install dependencies:**
   Open your terminal at the root and install the required packages:
   ```bash
   pip install -r requirements.txt

2. **Run the script:**
   ```bash
   python main.py -d <target_directory_path>