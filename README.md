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

## Screens & Widgets

The dashboard shows a sequence of screens. Each screen holds a number of widgets of different types. There are two supported types at the moment: table and picture.

Screens and widgets are defined in a template file `screens.mustache`:

Screens are shown for a few seconds and are then faded out. You can determine how long a screen is shown:

````
screens:
 - name: week
   title: Week 2021-31
   duration: 5
   widgets:
    - name: visits_version_ios
      ...
````

In this example, the screen named `week` is shown for 5 seconds.

Widgets can display dynamic data from an external source. Here is an example of a table widget:

````
- name: android
    title: Android News App
    type: table
    title_column: true
    data:
    - [ 'Current release', '{{ apps.news.platforms.android.distributions.google.releases.latest.tag }}' ]
    - [ 'date', '{{ apps.news.platforms.android.distributions.google.releases.latest.release_date }}' ]
````

As you can see in this example, widgets have a title and type, followed by a payload specific for the widget type. In the case of a table widget, the table data is passed as an array of rows with two columns. Column data may either be static or - as shown in the example - come from an external data source.

Here is an example of a picture widget:

````
- name: visits_version_ios
    title: "iOS: Visits by version"
    type: picture
    caption: "Visits total: 123_456"
    image: os_ios_2021-31.png
````

The payload in this case consists of an image URL and a caption.

For more examples, see the file [examples/screens.mustache](examples/screens.mustache) in this repository.

## Keys

Normally, the dashboard cycles through the screens without user interaction. However, using a keyboard, you can interrupt the progression, manually flip through the screens, or blank the screen:

* Q - quit
* Z - Blank screen
* SPACE - start/stop progression through the screens
* LEFT/RIGHT - flip through the screens and stop the progression

## Ideas

Can use https://github.com/brunosantanaa/pygame-dashboard

