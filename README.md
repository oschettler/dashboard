# Dashboard

This is a small dashboard. It runs on a Raspberry Pi Zero on my physical desk. But it runs on a desktop machine, too.

The screens are defined in a mustache template. The data are read from a URL and are updated once a minute.
The locations for both are defined in config.py.

## Installation

To easily separate the generic code from my local configuration, I use this setup:

````bash
mkdir dashboard
cd dashboard
git submodule add git@github.com:oschettler/dashboard.git
python3 -mvenv env
source env/bin/activate
pip install -r dashboard/requirements.txt
cp dashboard/examples/* .

# edit config.yaml and screens.mustache as required for your local configuration

python dashboard/dashboard.py
````

## Keys

* Q - quit
* Z - Blank screen
* SPACE - start/stop progression through the screens
* LEFT/RIGHT - flip through the screens and stop the progression

## Ideas

Can use https://github.com/brunosantanaa/pygame-dashboard

