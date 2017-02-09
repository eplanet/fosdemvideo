fosdemvideo
===========
Video crawler for downloading all FOSDEM videos from a given year. It leverages the XML schedule that can be found at: https://fosdem.org/YEAR/schedule/xml.

# Requirements
The crawler makes use of lxml Python package, that can be installed on Debian with `python3-lxml`.

Installing virtualenv is optional but recommended.

With the following packages you're good to go:
```bash
sudo apt-get install python3 python3-lxml python3-virtualenv
```

# Usage
Prefered way would be to start virtualenv with provided script:
```bash
source ./start_virtualenv.sh
./fosdem-video-crawler.py -h
```

