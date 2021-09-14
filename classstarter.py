# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
from os import system

import mouse
import pyautogui

from File import File
from table_maker import print_table


def zoom_auto():  # auto click-starting zoom application from browser

    exi = False
    def exit():
        global exi 
        exi = True
    mouse.on_click(exit)

    for i in range(20):
        if exi:
            break
        
        if joinm := pyautogui.locateOnScreen("imgs\\zoom_join2.png", confidence=0.9, grayscale=True):
            joinm_l = pyautogui.center(joinm)
            pyautogui.click(*joinm_l)

            for j in range(20):
                if pyautogui.locateOnScreen("imgs\\zoom_mic2.png", confidence=0.9, grayscale=True):
                    break
                else:
                    if mic := pyautogui.locateOnScreen("imgs\\zoom_mic1.png", confidence=0.9, grayscale=True):
                        mic_l = pyautogui.center(mic)
                        pyautogui.click(*mic_l)
                        break
            break
        elif joins := pyautogui.locateOnScreen("imgs\\zoom_join1.png", confidence=0.9, grayscale=True):
            joins_l = pyautogui.center(joins)
            pyautogui.click(*joins_l)
        time.sleep(3)
    mouse.unhook_all()


def gmeet_auto():  # auto click-starting google meet web application

    exi = False
    def exit():
        global exi 
        exi = True
    mouse.on_click(exit)

    gmeet_cam, gmeet_mic = False, False
    for i in range(20):
        if exi:
            break

        if gmeet_mic and gmeet_cam:
            if joinm := pyautogui.locateOnScreen("imgs\\gmeet_join.png", confidence=0.9, grayscale=True):
                joinm_l = pyautogui.center(joinm)
                pyautogui.click(*joinm_l)
                break

        else:
            if not gmeet_cam:
                if cam := pyautogui.locateOnScreen("imgs\\gmeet_cam.png", confidence=0.9, grayscale=True):
                    cam_l = pyautogui.center(cam)
                    pyautogui.click(*cam_l)
                    gmeet_cam = True
            if not gmeet_mic:
                if mic := pyautogui.locateOnScreen("imgs\\gmeet_mic.png", confidence=0.9, grayscale=True):
                    mic_l = pyautogui.center(mic)
                    pyautogui.click(*mic_l)
                    gmeet_mic = True
        time.sleep(3)
    mouse.unhook_all()


def start(link):
    # automating the clicks for joining the class
    system(f"start {link}")
    time.sleep(10)
    if "zoom" in link:
        zoom_auto()
    elif "meet" in link:
        gmeet_auto()


def start_auto():
    file = File("stor.txt")
    now = datetime.now()
    for i in list(file.val):
        td = datetime.fromisoformat(i["from"]) - now
        if timedelta(0) <= td <= timedelta(minutes=30):  # next class within next half hour
            print("Waiting for class...")
            print_table(i, keys=list(i.keys()), header=["Start", "Finish", "Link"])
            time.sleep(td.seconds-60)
            start(i['url'])
        elif now > datetime.fromisoformat(i["to"]):
            file.del_rec(i)


def start_manual():
    file = File("stor.txt")
    now = datetime.now()
    for i in list(file.val):
        to = datetime.fromisoformat(i["to"])+timedelta(minutes=5)
        fro = datetime.fromisoformat(i["from"])-timedelta(minutes=1)
        if fro <= now <= to:  # starting class between class timings
            print_table(i, keys=list(i.keys()), header=["Start", "Finish", "Link"])
            start(i['url'])
            return True
        elif now > to:
            file.del_rec(i)


if __name__ == "__main__":
    start_manual()
