import time
from typing import Tuple

import PIL
import pyautogui
import argparse
import webbrowser


def get_pixel_position_from_pin() -> pyautogui.Point:
    pixel = pyautogui.locateCenterOnScreen("imgs/pin.png", confidence=0.99)
    return pyautogui.Point(pixel.x, pixel.y + 24)


def get_closest_in_palette_index(color: tuple[int, int, int, int]) -> int:
    if color[3] < 128:
        return len(palette) -1
    closest = None
    min_distance = float("inf")
    for i in range(len(palette)):
        distance = (abs(color[0] - palette[i][0]) +
                    abs(color[1] - palette[i][1]) +
                    abs(color[2] - palette[i][2]))
        if distance < min_distance:
            min_distance = distance
            closest = i
    return closest


class XeniatorCalibration:
    zeroPos = None
    stepHorizontal = 0
    stepVertical = 0
    xOffset = 0
    yOffset = 0

    def calibration_sequence(self):
        x1, y1 = map(int, input("klikni na početni piksel i daj koordinate (x,y):").split(","))
        cl1 = get_pixel_position_from_pin()

        pyautogui.moveTo((cl1.x, cl1.y))

        x2, y2 = map(int, input("klikni na neki piksel dolje desno od pocetnog i daj koordinate (x,y):").split(","))
        cl2 = get_pixel_position_from_pin()

        pyautogui.moveTo((cl2.x, cl2.y))
        self.zeroPos = cl1
        self.stepHorizontal = (cl2.x - cl1.x) / (x2 - x1)
        self.stepVertical = (cl2.y - cl1.y) / (y2 - y1)
        self.xOffset = 0
        self.yOffset = 0
        print("kalibriraj ovo cudo TwT")
        print()
        print("r - prodđi po dijagonali")
        print("x+1, x-2, y+3, y-4 - promjeni offset za smjer")
        print("10 - odi ovolko po dijagonali")
        print("f - zavrsi kalibraciju")
        while True:
            c = input()
            if c == "r":
                for i in range(150):
                    pyautogui.click(self.get_coordinate_pixel(i, i))
                    time.sleep(.1)
            elif c[0] == "x":
                self.xOffset += int(c[1:])
                print(self.xOffset)
            elif c[0] == "y":
                self.yOffset += int(c[1:])
                print(self.yOffset)
            elif c == "f":
                break
            else:
                i = int(c)
                self.get_coordinate_pixel(i, i)
        print("yay, kalibracija gotova :3")

    def get_coordinate_pixel(self, x, y) -> pyautogui.Point:
        return pyautogui.Point(
            round(self.zeroPos.x + x * self.stepHorizontal) + self.xOffset,
            round(self.zeroPos.y + y * self.stepVertical) + self.yOffset)


print("otvara se link :3")
# webbrowser.open("https://wplace.live/", new=0, autoraise=True)
print("prijavi se UwU")
print("pazi da je donji desni kut slike vidljiv na platnu :>")

ap = argparse.ArgumentParser()
ap.add_argument("--click-delay", "-cd", type=int, help="time between clicks (ms)")

args = ap.parse_args()
clickDelay = args.click_delay / 1000
img = PIL.Image.open('img.png')
palette = [(0, 0, 0, 255),
           (60, 60, 60, 255),
           (120, 120, 120, 255),
           (210, 210, 210, 255),
           (255, 255, 255, 255),
           (96, 0, 24, 255),
           (237, 28, 36, 255),
           (255, 127, 39, 255),
           (246, 170, 9, 255),
           (249, 221, 59, 255),
           (255, 250, 188, 255),
           (14, 185, 104, 255),
           (19, 230, 123, 255),
           (135, 255, 94, 255),
           (12, 129, 110, 255),
           (16, 174, 166, 255),
           (19, 225, 190, 255),
           (40, 80, 158, 255),
           (64, 147, 228, 255),
           (96, 247, 242, 255),
           (107, 80, 246, 255),
           (153, 177, 251, 255),
           (120, 12, 153, 255),
           (170, 56, 185, 255),
           (224, 159, 249, 255),
           (203, 0, 122, 255),
           (236, 31, 128, 255),
           (243, 141, 169, 255),
           (104, 70, 52, 255),
           (149, 104, 42, 255),
           (248, 178, 119, 255),
           (0, 0, 0, 0)]
locIcon = pyautogui.locateCenterOnScreen("imgs/location.png", grayscale=True, confidence=0.95)
xIcon = pyautogui.locateCenterOnScreen("imgs/x.png", grayscale=True, confidence=0.95)

xc = XeniatorCalibration()
xc.calibration_sequence()

pyautogui.click(xIcon, duration=clickDelay)
time.sleep(2)
paintIcon = pyautogui.locateCenterOnScreen("imgs/brush.png", grayscale=True, confidence=0.95)
pyautogui.click(paintIcon, duration=clickDelay)

width, _ = pyautogui.size()
p = img.load()
w, h = img.size
currentColorIndex = -1
for i in range(h):
    for ii in range(w):
        if p[ii, i][-1] == 0:
            continue
        colorIndex = get_closest_in_palette_index(p[ii, i])
        if currentColorIndex != colorIndex:
            pyautogui.click(40 + colorIndex * (1840 / 31), 930, duration=clickDelay)
            currentColorIndex = colorIndex

        pyautogui.click(xc.get_coordinate_pixel(ii, i), duration=clickDelay)
