# -*- coding: utf-8 -*-
# author: Jeffz615
import tkinter as tk
import tkinter.messagebox
import win32api
import win32con

try:
    screenWidth = win32api.GetSystemMetrics(0)
    screenHeight = win32api.GetSystemMetrics(1)
    regeditKey = win32api.RegOpenKey(
        win32con.HKEY_CURRENT_USER, r'Software\miHoYo\原神', 0, win32con.KEY_ALL_ACCESS)
    regHeight = win32api.RegQueryValueEx(
        regeditKey, 'Screenmanager Resolution Height_h2627697771')[0]
    regWidth = win32api.RegQueryValueEx(
        regeditKey, 'Screenmanager Resolution Width_h182942802')[0]
    regFullScreen = win32api.RegQueryValueEx(
        regeditKey, 'Screenmanager Is Fullscreen mode_h3981298716')[0]
except:
    exit(1)


def on_closing():
    win32api.RegCloseKey(regeditKey)
    window.destroy()


window = tk.Tk()
window.title("原神 PC端 分辨率 修改工具")
window.geometry("400x60")
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
width.set(regWidth)


heightLabel = tk.Label(window, text='高 Height')
heightLabel.place(x=0.5, y=25)


height = tk.StringVar()
heightEntry = tk.Entry(window, show=None, textvariable=height)
heightEntry.place(x=75, y=25)
height.set(regHeight)


flag = tk.IntVar()
fullscreenCheckbutton = tk.Checkbutton(
    window, text='全屏显示 FullScreen', variable=flag, onvalue=1, offvalue=0)
fullscreenCheckbutton.place(x=250, y=0.5)
flag.set(regFullScreen)


def main():
    global regWidth
    global regHeight
    global regFullScreen
    widthNum = width.get()
    heightNum = height.get()
    isfullScreen = int(bool(flag.get()))
    if check(widthNum) and check(heightNum):
        widthNum = int(widthNum)
        heightNum = int(heightNum)
        if not (int(widthNum) <= screenWidth and int(heightNum) <= screenHeight):
            tkinter.messagebox.showerror(
                title='Error', message='Width/Height 超出屏幕尺寸.')
            return
    else:
        tkinter.messagebox.showerror(
            title='Error', message='Width/Height Error.')
        return
    msgbox = False
    if widthNum != regWidth:
        try:
            win32api.RegSetValueEx(
                regeditKey, 'Screenmanager Resolution Width_h182942802', 0, win32con.REG_DWORD, widthNum)
            regWidth = win32api.RegQueryValueEx(
                regeditKey, 'Screenmanager Resolution Width_h182942802')[0]
            msgbox = True
        except:
            tkinter.messagebox.showerror(
                title='Error', message='Regedit I/O Error.')
            exit(1)
    if heightNum != regHeight:
        try:
            win32api.RegSetValueEx(
                regeditKey, 'Screenmanager Resolution Height_h2627697771', 0, win32con.REG_DWORD, heightNum)
            regHeight = win32api.RegQueryValueEx(
                regeditKey, 'Screenmanager Resolution Height_h2627697771')[0]
            msgbox = True
        except:
            tkinter.messagebox.showerror(
                title='Error', message='Regedit I/O Error.')
            exit(1)
    if isfullScreen != regFullScreen:
        try:
            win32api.RegSetValueEx(
                regeditKey, 'Screenmanager Is Fullscreen mode_h3981298716', 0, win32con.REG_DWORD, isfullScreen)
            regFullScreen = win32api.RegQueryValueEx(
                regeditKey, 'Screenmanager Is Fullscreen mode_h3981298716')[0]
            msgbox = True
        except:
            tkinter.messagebox.showerror(
                title='Error', message='Regedit I/O Error.')
            exit(1)
    if msgbox:
        tkinter.messagebox.showinfo(title='Info', message='Success!')


submit = tk.Button(window, text='完成 Submit', command=main)
submit.place(x=250, y=25)

window.mainloop()
