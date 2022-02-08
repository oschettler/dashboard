#!python

'''
A small dashboard, perfect for a wall-mounted display

Author: Olav Schettler
License: MIT
'''

import math
import os.path
import pygame
import pgzrun
import yaml
from datetime import datetime
import requests

import chevron

WIDTH = 1024
HEIGHT = 600
darkgray=(40,40,40)
middlegray=(80,80,80)

screen_index = 0
current_screen = None
auto = True
blank = False
#next_screen = None
seconds_left = 0

screens = None

last_update = { 'date': None, 'time': None }


def show_picture(widget, box):
    screen.draw.text(widget['caption'],
                     left=box.x + 20,
                     top=box.y + 30,
                     width=box.w - 40,
                     background='black',
                     color='white',
                     fontsize=30,
                     align='left')
    img = pygame.image.load(os.path.join('images', widget['image']))
    w, h = img.get_size()
    if w > box.w - 40:
        new_w = box.w - 40
        new_h = int(new_w / w * h)
        img = pygame.transform.scale(img, (new_w, new_h))
    screen.blit(img, (box.x + 20, box.y + 80))


def show_table(widget, box):
    dt = datetime.now()
    today = dt.strftime('%Y-%m-%d')
    now = dt.strftime('%H:%M')

    data = widget['data']

    for y, row in enumerate(data):
        for x, text in enumerate(row):
            rendered_text = text.format(**locals())
            w = box.w / len(row) - 40
            h = 30 # box.h / len(data)

            if widget['title_column'] and x == 0:
                screen.draw.text(rendered_text,
                                 right=box.x + (x+1) * w,
                                 top=box.y + 30 + y * h,
                                 width=w,
                                 background='black',
                                 color='gray',
                                 fontsize=30,
                                 align='right'
                )
            else:
                screen.draw.text(rendered_text,
                                 left=box.x + 20 + x * w,
                                 top=box.y + 30 + y * h,
                                 width=w,
                                 background='black',
                                 color='white',
                                 fontsize=30,
                                 align='left'
                )


def show_widget(widget, box):
    frame = Rect(box.x+8, box.y+14, box.w-16, box.h-16)
    screen.draw.rect(frame, color=darkgray)
    screen.draw.text(widget['title'],
                     centerx=box.x + box.w / 2,
                     top=box.y,
                     align='center',
                     color='gray',
                     background='black',
                     fontsize=40,
    )
    if widget['type'] == 'table':
        show_table(widget, frame)
    elif widget['type'] == 'picture':
        show_picture(widget, frame)
    

def show_screen(scr):
    screen.clear()
    screen.draw.filled_rect(Rect(0, 16, WIDTH-1, 4), color=darkgray)
    screen.draw.filled_rect(Rect(0, 26, WIDTH-1, 4), color=darkgray)
    screen.draw.text(scr['title'],
                     centerx=WIDTH / 2,
                     top=0,
                     align='center',
                     color='gray',
                     background='black',
                     fontsize=60)

    for i, widget in enumerate(scr['widgets']):
        n = len(scr['widgets'])
        w = WIDTH / 2
        h = (HEIGHT - 60) / math.ceil(n / 2)
        y = 40 + i // 2 * h
        x = i % 2 * w
        show_widget(widget, Rect(x, y, w, h))

    screen.draw.text(last_update['date'] + ' ' + last_update['time'],
                     right=WIDTH - 16,
                     bottom=HEIGHT - 12,
                     fontsize=30,
                     color=middlegray,
                     background='black')
    screen.draw.text(str(screen_index + 1),
                     left=50,
                     bottom=HEIGHT - 12,
                     fontsize=30,
                     color=middlegray,
                     background='black')
    if auto:
        width = seconds_left / current_screen['duration'] * 80 
        screen.draw.filled_rect(Rect(
            (80, HEIGHT-28), (width, 10)
        ), 'gray')
    else:
        screen.draw.filled_circle((30, HEIGHT-24), 10, 'red')
    

config = yaml.load(
    open('config.yaml'),
    Loader=yaml.FullLoader)
TITLE = config['title'] if 'title' in config else 'Dashboard'

def on_key_down(key, mod, unicode):
    global screen_index, auto, blank
    if key == keys.Q:
        quit()
    if key == keys.SPACE:
        auto = not auto
    if key == keys.Z:
        blank = not blank
    if key == keys.LEFT:
        auto = False
        screen_index -= 1
        if screen_index < 0:
            screen_index = len(screens['screens']) - 1 
    if key == keys.RIGHT:
        auto = False
        screen_index += 1
        if screen_index >= len(screens['screens']):
            screen_index = 0
    setup_screen()


def update(dt):
    global seconds_left
    if seconds_left > 0:
        seconds_left -= dt


def draw():
    if blank:
        screen.clear()
    elif current_screen:
        show_screen(current_screen)

def fade():
    mask = pygame.Surface((WIDTH, HEIGHT))
    mask.fill((0,0,0))
    for alpha in range(0, 256, 40): # On a raspberry pi zero this is quite slow
        mask.set_alpha(alpha)
        draw()
        screen.blit(mask, (0,0))
        pygame.display.update()
        #pygame.time.delay(1)


def switch_screens():
    global screen_index, current_screen
    screen_index += 1
    if screen_index >= len(screens['screens']):
        screen_index = 0
    #print("Switch...")
    fade()
    setup_screen()


def setup_screen():
    global current_screen, seconds_left
    #print("...Setup")
    current_screen = screens['screens'][screen_index]

    if auto:
        duration = current_screen['duration'] \
            if 'duration' in current_screen else 2
        seconds_left = duration
        clock.schedule_unique(switch_screens, duration)
    else:
        clock.unschedule(switch_screens)


def load_screens():
    global screens, last_update
    
    r = requests.get(config['data_url'])
    if r.status_code != 200:
        print("...failed", r.status_code)
    data = yaml.load(r.text, Loader=yaml.FullLoader)

    with open(config['screens_template']) as f:
        screens = yaml.load(chevron.render(f, data), Loader=yaml.FullLoader)

    dt = datetime.now()
    last_update['date'] = dt.strftime('%Y-%m-%d')
    last_update['time'] = dt.strftime('%H:%M')

    
clock.schedule_interval(load_screens, 60)

pygame.mouse.set_visible(False)
load_screens()
setup_screen()
pgzrun.go()
