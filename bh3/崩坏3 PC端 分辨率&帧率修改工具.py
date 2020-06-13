# -*- coding: utf-8 -*-
# author: Jeffz615

import tkinter as tk
import tkinter.messagebox
import win32api
import win32con
import json


def loadreg():
    global regeditKey, regeditJson, regFrame, regWidth, regHeight, regFullscreen
    regeditKey = win32api.RegOpenKey(
        win32con.HKEY_CURRENT_USER, r'Software\miHoYo\崩坏3', 0, win32con.KEY_ALL_ACCESS)
    regeditJson = json.loads(win32api.RegQueryValueEx(
        regeditKey, 'GENERAL_DATA_V2_ScreenSettingData_h1916288658')[0][:-1])
    regFrame = json.loads(win32api.RegQueryValueEx(
        regeditKey, 'GENERAL_DATA_V2_PersonalGraphicsSetting_h906361411')[0][:-1])
    regWidth = win32api.RegQueryValueEx(
        regeditKey, 'Screenmanager Resolution Width_h182942802')[0]
    regHeight = win32api.RegQueryValueEx(
        regeditKey, 'Screenmanager Resolution Height_h2627697771')[0]
    regFullscreen = win32api.RegQueryValueEx(
        regeditKey, 'Screenmanager Is Fullscreen mode_h3981298716')[0]
    if regWidth != regeditJson['width']:
        win32api.RegSetValueEx(
            regeditKey, 'Screenmanager Resolution Width_h182942802', 0, win32con.REG_DWORD, regWidth)
        regWidth = regeditJson['width']
    if regHeight != regeditJson['height']:
        win32api.RegSetValueEx(
            regeditKey, 'Screenmanager Resolution Height_h2627697771', 0, win32con.REG_DWORD, regHeight)
        regHeight = regeditJson['height']
    if regFullscreen != int(regeditJson['isfullScreen']):
        win32api.RegSetValueEx(
            regeditKey, 'Screenmanager Is Fullscreen mode_h3981298716', 0, win32con.REG_DWORD, int(regFullscreen))
        regFullscreen = regeditJson['isfullScreen']


try:
    endByte = b'\x00'
    screenWidth = win32api.GetSystemMetrics(0)
    screenHeight = win32api.GetSystemMetrics(1)
    loadreg()
except:
    exit(1)


def on_closing():
    win32api.RegCloseKey(regeditKey)
    window.destroy()


window = tk.Tk()
window.title("崩坏3 PC端 分辨率&帧率 修改工具")
window.geometry("400x140")
window.protocol("WM_DELETE_WINDOW", on_closing)
window.resizable(0, 0)


def check(context):
    if context.isdigit() or context == "":
        return True
    else:
        return False


widthLabel = tk.Label(window, text='宽 Width')
widthLabel.place(x=0.5, y=0.5)


width = tk.StringVar()
widthEntry = tk.Entry(window, show=None, textvariable=width)
widthEntry.place(x=75, y=0.5)
width.set(regeditJson['width'])


heightLabel = tk.Label(window, text='高 Height')
heightLabel.place(x=0.5, y=25)


height = tk.StringVar()
heightEntry = tk.Entry(window, show=None, textvariable=height)
heightEntry.place(x=75, y=25)
height.set(regeditJson['height'])


TargetFrameRateForInLevelLabel = tk.Label(
    window, text='关卡内帧率 TargetFrameRateForInLevel')
TargetFrameRateForInLevelLabel.place(x=0.5, y=49.5)


TargetFrameRateForInLevel = tk.StringVar()
TargetFrameRateForInLevelEntry = tk.Entry(
    window, show=None, textvariable=TargetFrameRateForInLevel)
TargetFrameRateForInLevelEntry.place(x=240, y=49.5)
TargetFrameRateForInLevel.set(regFrame['TargetFrameRateForInLevel'])


TargetFrameRateForOthersLabel = tk.Label(
    window, text='关卡外帧率 TargetFrameRateForOthers')
TargetFrameRateForOthersLabel.place(x=0.5, y=74)


TargetFrameRateForOthers = tk.StringVar()
TargetFrameRateForOthersEntry = tk.Entry(
    window, show=None, textvariable=TargetFrameRateForOthers)
TargetFrameRateForOthersEntry.place(x=240, y=74)
TargetFrameRateForOthers.set(regFrame['TargetFrameRateForOthers'])


flag = tk.IntVar()
fullscreenCheckbutton = tk.Checkbutton(
    window, text='全屏显示 FullScreen', variable=flag, onvalue=1, offvalue=0)
fullscreenCheckbutton.place(x=250, y=0.5)
flag.set(regeditJson['isfullScreen'])


def main():
    global regeditJson, regFrame, regWidth, regHeight, regFullscreen
    widthNum = width.get()
    heightNum = height.get()
    isfullScreen = bool(flag.get())
    frame1 = TargetFrameRateForInLevel.get()
    frame2 = TargetFrameRateForOthers.get()
    if check(widthNum) and check(heightNum) and check(frame1) and check(frame2):
        widthNum = int(widthNum)
        heightNum = int(heightNum)
        frame1 = int(frame1)
        frame2 = int(frame2)
        if not (int(widthNum) <= screenWidth and int(heightNum) <= screenHeight):
            tkinter.messagebox.showerror(
                title='Error', message='Width/Height 超出屏幕尺寸.')
            return
    else:
        tkinter.messagebox.showerror(
            title='Error', message='Width/Height Error.')
        return
    if widthNum != regeditJson['width'] or heightNum != regeditJson['height'] or isfullScreen != regeditJson['isfullScreen'] or frame1 != regFrame['TargetFrameRateForInLevel'] or frame2 != regFrame['TargetFrameRateForOthers']:
        value = bytes(json.dumps({'width': widthNum, 'height': heightNum,
                                  'isfullScreen': isfullScreen}), encoding='utf-8') + endByte
        regFrame['TargetFrameRateForInLevel'] = frame1
        regFrame['TargetFrameRateForOthers'] = frame2
        frameJson = bytes(json.dumps(regFrame), encoding='utf-8') + endByte
        try:
            win32api.RegSetValueEx(
                regeditKey, 'GENERAL_DATA_V2_ScreenSettingData_h1916288658', 0, win32con.REG_BINARY, value)
            win32api.RegSetValueEx(
                regeditKey, 'Screenmanager Resolution Width_h182942802', 0, win32con.REG_DWORD, widthNum)
            win32api.RegSetValueEx(
                regeditKey, 'Screenmanager Resolution Height_h2627697771', 0, win32con.REG_DWORD, heightNum)
            win32api.RegSetValueEx(
                regeditKey, 'Screenmanager Is Fullscreen mode_h3981298716', 0, win32con.REG_DWORD, int(isfullScreen))
            win32api.RegSetValueEx(
                regeditKey, 'GENERAL_DATA_V2_PersonalGraphicsSetting_h906361411', 0, win32con.REG_BINARY, frameJson)
            loadreg()
            tkinter.messagebox.showinfo(title='Info', message='Success!')
        except:
            tkinter.messagebox.showerror(
                title='Error', message='Regedit I/O Error.')
            exit(1)


submit = tk.Button(window, text='完成 Submit', command=main)
submit.place(x=250, y=100)

window.mainloop()
