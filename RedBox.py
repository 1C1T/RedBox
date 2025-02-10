# -*- coding: utf-8 -*-
#    作者  :  Limit
#    企鹅  :  599772335
#    群聊  :  928286446
#    日期  :  2025.2.10
# ---------------------

import os
import re
import sys
import time
import ctypes
import winreg
import psutil
import inspect
import pystray
import threading
import subprocess
import tkinter as tk
import tkinter.font as tk_font
from tkinter import (messagebox, filedialog, ttk)
from tkinter.colorchooser import askcolor
from yaml import (load, dump, FullLoader)
from pygments.lexers import LuaLexer
from pygments import lex
from ctypes import wintypes
from PIL import Image
from lua51 import LuaRuntime
from pynput import (mouse, keyboard)

# 定义一个全局字典用于保存变量 GV = Global Variable
GV = {
    "THREAD_ID" : 0,# 线程ID
    "THREAD_PAUSE" : False,# 脚本运行暂停信号
    "TEXT" : "",# 输入的脚本内容
    "ENABLE_MOUSE_LEFT" : False,# 1 或 true 以启用鼠标按键 1 事件报告
    "MOUSE_LEFT" : 0,# 左键
    "MOUSE_RIGHT" : 0,# 右键
    "MOUSE_MIDDLE" : 0,# 中键
    "MOUSE_WHEEL" : 0,# 滚轮键
    "MOUSE_SIDE_X1" : 0,# 后侧键x1
    "MOUSE_SIDE_X2" : 0,# 前侧键x2
    "LAST_KEY_CLICK" : "",# 最后一次单击的键盘按键
    "KEYBOARD_LEFT_SHIFT" : 0,# 左 Shift键
    "KEYBOARD_RIGHT_SHIFT" : 0,# 右 Shift键
    "KEYBOARD_LEFT_CTRL" : 0,# 左 Ctrl键
    "KEYBOARD_RIGHT_CTRL" : 0,# 右 Ctrl键
    "KEYBOARD_LEFT_ALT" : 0,# 左 Alt键
    "KEYBOARD_RIGHT_ALT" : 0,# 右 Alt键
    "START_TIME" : 0,# lua脚本运行时间记录
    "EVENT" : "",# 该字符串包含了用户所触发的事件名称 如：MOUSE_BUTTON_PRESSED
    "ARG" : 0,# 与事件标识符相对应的参数值 如：1
    "FAMILY" : "",# 触发硬件事件的设备族 如：mouse
    "LAST_EVENT" : "",# 最后一次EVENT
    "LAST_ARG" : 0,# 最后一次ARG
    "LAST_FAMILY" : "",# 最后一次FAMILY

}


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class SendInputApi:#键盘鼠标模拟API
    def __init__(self):
        self.SendInput = ctypes.windll.user32.SendInput
        self.KEYBOARD_MAPPING = {# 键盘扫描码映射
            'escape': 0x01,
            'esc': 0x01,
            'f1': 0x3B,
            'f2': 0x3C,
            'f3': 0x3D,
            'f4': 0x3E,
            'f5': 0x3F,
            'f6': 0x40,
            'f7': 0x41,
            'f8': 0x42,
            'f9': 0x43,
            'f10': 0x44,
            'f11': 0x57,
            'f12': 0x58,
            'printscreen': 0xB7,
            'prntscrn': 0xB7,
            'prtsc': 0xB7,
            'prtscr': 0xB7,
            'scrolllock': 0x46,
            'pause': 0xC5,
            '`': 0x29,
            '1': 0x02,
            '2': 0x03,
            '3': 0x04,
            '4': 0x05,
            '5': 0x06,
            '6': 0x07,
            '7': 0x08,
            '8': 0x09,
            '9': 0x0A,
            '0': 0x0B,
            '-': 0x0C,
            '=': 0x0D,
            'backspace': 0x0E,
            'insert': 0xD2 + 1024,
            'home': 0xC7 + 1024,
            'pageup': 0xC9 + 1024,
            'pagedown': 0xD1 + 1024,
            # 数字键盘
            'numlock': 0x45,
            'divide': 0xB5 + 1024,
            'multiply': 0x37,
            'subtract': 0x4A,
            'add': 0x4E,
            'decimal': 0x53,
            'numpadenter': 0x9C + 1024,
            'numpad1': 0x4F,
            'numpad2': 0x50,
            'numpad3': 0x51,
            'numpad4': 0x4B,
            'numpad5': 0x4C,
            'numpad6': 0x4D,
            'numpad7': 0x47,
            'numpad8': 0x48,
            'numpad9': 0x49,
            'numpad0': 0x52,
            # 大键盘
            'tab': 0x0F,
            'q': 0x10,
            'w': 0x11,
            'e': 0x12,
            'r': 0x13,
            't': 0x14,
            'y': 0x15,
            'u': 0x16,
            'i': 0x17,
            'o': 0x18,
            'p': 0x19,
            '[': 0x1A,
            ']': 0x1B,
            '\\': 0x2B,
            'del': 0xD3 + 1024,
            'delete': 0xD3 + 1024,
            'end': 0xCF + 1024,
            'capslock': 0x3A,
            'a': 0x1E,
            's': 0x1F,
            'd': 0x20,
            'f': 0x21,
            'g': 0x22,
            'h': 0x23,
            'j': 0x24,
            'k': 0x25,
            'l': 0x26,
            ';': 0x27,
            "'": 0x28,
            'enter': 0x1C,
            'return': 0x1C,
            'shift': 0x2A,
            'shiftleft': 0x2A,
            'z': 0x2C,
            'x': 0x2D,
            'c': 0x2E,
            'v': 0x2F,
            'b': 0x30,
            'n': 0x31,
            'm': 0x32,
            ',': 0x33,
            '.': 0x34,
            '/': 0x35,
            'shiftright': 0x36,
            'ctrl': 0x1D,
            'ctrlleft': 0x1D,
            'win': 0xDB + 1024,
            'winleft': 0xDB + 1024,
            'alt': 0x38,
            'altleft': 0x38,
            ' ': 0x39,
            'space': 0x39,
            'altright': 0xB8 + 1024,
            'winright': 0xDC + 1024,
            'apps': 0xDD + 1024,
            'ctrlright': 0x9D + 1024,
            'up': ctypes.windll.user32.MapVirtualKeyW(0x26, 0),
            'left': ctypes.windll.user32.MapVirtualKeyW(0x25, 0),
            'down': ctypes.windll.user32.MapVirtualKeyW(0x28, 0),
            'right': ctypes.windll.user32.MapVirtualKeyW(0x27, 0),
        }

    def _to_windows_coordinates(self, x=0, y=0):#返回(x, y)的准确值
        display_width, display_height = self.size()
        windows_x = (x * 65536) // display_width + 1
        windows_y = (y * 65536) // display_height + 1
        return windows_x, windows_y

    def position(self):#获取鼠标(x, y)坐标
        cursor = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
        return self._to_windows_coordinates(cursor.x, cursor.y)

    def size(self):#返回屏幕窗口大小
        return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

    def mouseDown(self, button=1):#按下鼠标按键，默认鼠标左键
        ev = 0x0002
        if button == 1:#左键
            ev = 0x0002
        elif button == 2:#中键
            ev = 0x0020
        elif button == 3:#右键
            ev = 0x0008
        else:
            raise ValueError('按钮参数必须是1(左键)、2(中键)或3(右键)之一')

        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, ev, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        self.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def mouseUp(self, button=1):#弹起鼠标按键，默认鼠标左键
        ev = 0x0004
        if button == 1:#左键
            ev = 0x0004
        elif button == 2:#中键
            ev = 0x0040
        elif button == 3:#右键
            ev = 0x0010
        else:
            raise ValueError('按钮参数必须是1(左键)、2(中键)或3(右键)之一')

        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, ev, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        self.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def click(self, button=1):#点击鼠标按键，默认鼠标左键
        ev = 0x0006
        if button == 1:#左键
            ev = 0x0006
        elif button == 2:#中键
            ev = 0x0060
        elif button == 3:#右键
            ev = 0x0018
        else:
            raise ValueError('按钮参数必须是1(左键)、2(中键)或3(右键)之一')

        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, ev, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        self.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def moveTo(self, x=0, y=0):#鼠标绝对移动 相对屏幕左上角(0, 0)
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(x, y, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
        command = Input(ctypes.c_ulong(0), ii_)
        self.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

    def moveRel(self, xOffset=None, yOffset=None):#鼠标相对移动 相对当前鼠标位置
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(xOffset, yOffset, 0, 0x0001, 0, ctypes.pointer(extra))
        command = Input(ctypes.c_ulong(0), ii_)
        self.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

    def keyDown(self, key):#按下键盘按键
        if not key in self.KEYBOARD_MAPPING or self.KEYBOARD_MAPPING[key] is None:
            return

        keybdFlags = 0x0008

        # 初始化事件跟踪
        insertedEvents = 0
        expectedEvents = 1

        if key in ['up', 'left', 'down', 'right']:
            keybdFlags |= 0x0001
            if ctypes.windll.user32.GetKeyState(0x90):
                expectedEvents = 2
                hexKeyCode = 0xE0
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
                x = Input(ctypes.c_ulong(1), ii_)
                insertedEvents += self.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        hexKeyCode = self.KEYBOARD_MAPPING[key]
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        insertedEvents += self.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        return insertedEvents == expectedEvents

    def keyUp(self, key):#弹起键盘按键
        if not key in self.KEYBOARD_MAPPING or self.KEYBOARD_MAPPING[key] is None:
            return

        keybdFlags = 0x0008 | 0x0002

        # 初始化事件跟踪
        insertedEvents = 0
        expectedEvents = 1

        if key in ['up', 'left', 'down', 'right']:
            keybdFlags |= 0x0001

        hexKeyCode = self.KEYBOARD_MAPPING[key]
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        insertedEvents += self.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        if key in ['up', 'left', 'down', 'right'] and ctypes.windll.user32.GetKeyState(0x90):
            expectedEvents = 2
            hexKeyCode = 0xE0
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(1), ii_)
            insertedEvents += self.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        return insertedEvents == expectedEvents

    def press(self, keys, presses=1):#点击键盘按键
        if type(keys) == str:
            if len(keys) > 1:
                keys = keys.lower()
            keys = [keys]  # 如果keys是'enter'，则将其转换为['enter']。
        else:
            lowerKeys = []
            for s in keys:
                if len(s) > 1:
                    lowerKeys.append(s.lower())
                else:
                    lowerKeys.append(s)
            keys = lowerKeys

        # 我们需要按 x 键 y 次，总共需要按 x*y 次
        expectedPresses = presses * len(keys)
        completedPresses = 0

        for i in range(presses):
            for k in keys:
                downed = self.keyDown(k)
                upped = self.keyUp(k)
                # 如果成功“按下”和“按下”按键，则将按键视为完成
                if downed and upped:
                    completedPresses += 1

        return completedPresses == expectedPresses

    def typewrite(self, message):#打字机 连续点击键盘按键
        for c in message:
            if len(c) > 1:
                c = c.lower()
            self.press(c)


class SyntaxAndThemes:#主题

    def __init__(self, master):

        self.master = master

        self.monokaipro_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/monokai_pro.yaml'))
        self.monokai_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/monokai_ord.yaml'))
        self.gruvbox_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/gruvbox.yaml'))
        self.solarized_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/solarized.yaml'))
        self.darkheart_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/dark-heart.yaml'))
        self.githubly_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/githubly.yaml'))
        self.dracula_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/dracula.yaml'))
        self.pumpkin_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/pumpkin.yaml'))
        self.material_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/material.yaml'))
        self.desert_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/desert.yaml'))
        self.rust_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/rust.yaml'))
        self.deepBlack_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/deep-black.yaml'))
        self.helloKitty_theme_path = master.parent.loader.resource_path(
            os.path.join('data', 'theme_configs/hello-kitty.yaml'))

        self.default_theme_path = self.darkheart_theme_path

    def load_default(self):
        self.master.load_new_theme(self.default_theme_path)

    def load_monokai_pro(self):
        self.master.load_new_theme(self.monokaipro_theme_path)

    def load_monokai(self):
        self.master.load_new_theme(self.monokai_theme_path)

    def load_gruvbox(self):
        self.master.load_new_theme(self.gruvbox_theme_path)

    def load_rust(self):
        self.master.load_new_theme(self.rust_theme_path)

    def load_solarized(self):
        self.master.load_new_theme(self.solarized_theme_path)

    def load_darkheart(self):
        self.master.load_new_theme(self.darkheart_theme_path)

    def load_githubly(self):
        self.master.load_new_theme(self.githubly_theme_path)

    def load_dracula(self):
        self.master.load_new_theme(self.dracula_theme_path)

    def load_pumpkin(self):
        self.master.load_new_theme(self.pumpkin_theme_path)

    def load_material(self):
        self.master.load_new_theme(self.material_theme_path)

    def load_desert(self):
        self.master.load_new_theme(self.desert_theme_path)

    def load_deepBlack(self):
        self.master.load_new_theme(self.deepBlack_theme_path)

    def load_helloKitty(self):
        self.master.load_new_theme(self.helloKitty_theme_path)

    def load_theme_from_config(self):# pt：从设置文件加载主题
        theme = self.master.parent.loader.load_settings_data()["theme"]
        self.master.load_new_theme(theme, 1)

    def save_theme_to_config(self, path):# 保存主题设置到配置文件
        loader = self.master.parent.loader
        data = loader.load_settings_data()
        last_theme = data["theme"]
        data["theme"] = path

        loader.store_settings_data(data)
        #修改主题子菜单
        theme_name = ["dark-heart", "dracula", "desert", "githubly", "gruvbox", "material", "monokai_ord", "monokai_pro", "pumpkin", "rust", "solarized", "deep-black", "hello-kitty"]
        theme_str = ["黑暗之心", "德古拉", "荒漠", "明亮", "矿箱", "材料", "莫诺凯", "莫诺凯+", "南瓜", "铁锈", "暗青", "深黑", "凯蒂"]
        for i in range(13):
            if theme_name[i] in last_theme:
                self.master.parent.menubar.theme_dropdown.entryconfig(i, label=theme_str[i])
            if theme_name[i] in path:
                self.master.parent.menubar.theme_dropdown.entryconfig(i, label="√ "+theme_str[i])


class SyntaxHighlighting():#语法高亮
    def __init__(self, parent, text_widget, initial_content):
        self.parent = parent
        self.syntax_and_themes = SyntaxAndThemes(self)
        self.settings = parent.settings
        self.text = text_widget
        self.font_family = parent.font_family
        self.font_size = parent.font_size
        self.previousContent = initial_content
        self.lexer = LuaLexer() # 设置默认语法为Lua
        self.comment_color = None
        self.string_color = None
        self.number_color = None
        self.keyword_color = None
        self.type_color = None
        self.operator_color = None
        self.bultin_function_color = None
        self.class_color = None
        self.namespace_color = None
        self.class_name_color = None
        self.function_name_color = None
        self.text_color = None
        self.thread_sign = None
        self.auto_highlight = True
        self.first_run = True
        self.completed_highlight = True
        self.bottom_rows = self.parent.scrolly.get()[1]
        threading.Thread(target=self.thread_always).start()# 开启自动高亮线程

    def initial_highlight(self, *args):
        if self.auto_highlight:#启用语法高亮时
            threading.Thread(target=self.thread_highlight, args=(*args, )).start()

    def thread_highlight(self, *args):
        if self.thread_sign:
            return
        self.thread_sign = True
        if self.first_run:
            time.sleep(0.3)
            # print("首次运行语法高亮1")
            self.first_run = None
        
        self.clear_existing_tags()#清除标签
        self.text.tag_configure('Token.Comment.Single', foreground=self.comment_color)#注释
        self.text.tag_configure('Token.Text', foreground=self.text_color)
        self.text.tag_configure('Token.Keyword.Namespace', foreground=self.namespace_color)#import
        self.text.tag_configure('Token.Name.Namespace', foreground=self.parent.font_color)#import 后的字符
        self.text.tag_configure('Token.Keyword', foreground=self.keyword_color)
        self.text.tag_configure('Token.Punctuation', foreground=self.bultin_function_color)
        self.text.tag_configure('Token.Name', foreground=self.parent.font_color)#import 后的字符
        self.text.tag_configure('Token.Operator', foreground=self.operator_color)
        self.text.tag_configure('Token.Literal.String.Double', foreground=self.string_color)
        self.text.tag_configure('Token.Literal.Number.Integer', foreground=self.number_color)
        self.text.tag_configure('Token.Comment.Multiline', foreground=self.comment_color)
        self.text.tag_configure('Token.Literal.String', foreground=self.string_color)
        self.text.tag_configure('Token.Literal.String.Char', foreground=self.string_color)
        self.text.tag_configure('Token.Literal.Number.Float', foreground=self.number_color)
        self.text.tag_configure('Token.Keyword.Type', foreground=self.type_color, font=self.parent.italics)
        self.text.tag_configure('Token.Keyword.Declaration', foreground=self.bultin_function_color, font=self.parent.italics)
        self.text.tag_configure('Token.Name.Class', foreground=self.class_name_color)
        self.text.tag_configure('Token.Text.Whitespace', foreground=self.parent.bg_color)
        self.text.tag_configure('Token.Name.Function', foreground=self.function_name_color)
        self.text.tag_configure('Token.Generic.Emph', font=self.parent.italics)
        self.text.tag_configure('Token.Generic.Strong', font=self.parent.bold)
        self.text.tag_configure('Token.Generic.Heading', font=self.parent.header1)
        self.text.tag_configure('Token.Generic.Subheading', font=self.parent.header2)
        self.text.tag_configure('Token.Name.Builtin.Pseudo', foreground=self.class_color, font=self.parent.italics)
        self.text.tag_configure('Token.Name.Builtin', foreground=self.bultin_function_color)
        self.text.tag_configure('Token.Punctuation.Indicator', foreground=self.bultin_function_color)
        self.text.tag_configure('Token.Literal.Scalar.Plain', foreground=self.number_color)
        self.text.tag_configure('Token.Literal.String.Single', foreground=self.string_color)
        self.text.tag_configure('Token.Keyword.Constant', foreground=self.number_color)
        self.text.tag_configure('Token.Literal.String.Interpol', foreground=self.string_color)
        self.text.tag_configure('Token.Name.Decorator', foreground=self.number_color)
        self.text.tag_configure('Token.Operator.Word', foreground=self.operator_color)
        self.text.tag_configure('Token.Literal.String.Affix', foreground=self.bultin_function_color)
        self.text.tag_configure('Token.Name.Function.Magic', foreground=self.bultin_function_color)
        self.text.tag_configure('Token.Literal.Number.Oct', foreground=self.number_color)
        self.text.tag_configure('Token.Keyword.Reserved', foreground=self.keyword_color)
        self.text.tag_configure('Token.Name.Attribute', foreground=self.bultin_function_color)
        self.text.tag_configure('Token.Name.Tag', foreground=self.namespace_color)
        self.text.tag_configure('Token.Comment.PreprocFile', forground=self.namespace_color)
        self.text.tag_configure('Token.Name.Label', foreground=self.class_color)
        self.text.tag_configure('Token.Literal.String.Escape', foreground=self.number_color)
        
        total_rows = float(self.text.index("end-1c"))
        float_top_rows = self.parent.scrolly.get()[0] * total_rows
        if float_top_rows == 0.0:
            float_top_rows = 1.0
        elif float_top_rows > 10:
            float_top_rows -= 10
        elif float_top_rows > 20:
            float_top_rows -= 20
        elif float_top_rows > 30:
            float_top_rows -= 30
        top_rows = str(float_top_rows).split(".")[0] + ".0"
        bottom_rows = str(self.parent.scrolly.get()[1] * total_rows + 30).split(".")[0] + ".0"
        data_start = self.text.get(top_rows, bottom_rows)
        is_line_break = None
        len_data_start = len(data_start)
        if len_data_start > 3000:# 字数太多会导致卡顿，超过3000个字符就停止语法高亮
            return
        elif len_data_start > 1:
            if data_start[0] == "\n":
                self.text.insert(top_rows, ' ')
                is_line_break = True
        data = self.text.get(top_rows, bottom_rows)
        self.text.mark_set("range_start", top_rows)
        counter = 0
        for token, content in lex(data, self.lexer):
            counter += 1
            if counter > 3000:
                break
            self.text.mark_set("range_end", "range_start + %dc" % len(content))
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")
        self.thread_sign = None
        if is_line_break:
            self.text.delete(top_rows, float_top_rows+0.1)

    def thread_always(self):
        while True:
            time.sleep(0.1)
            if self.auto_highlight and self.completed_highlight:#启用语法高亮时， 同时上一次语法高亮已完成
                now_bottom_rows = self.parent.scrolly.get()[1]
                if now_bottom_rows != self.bottom_rows:#说明画面移动了
                    self.bottom_rows = now_bottom_rows
                    if self.first_run:
                        continue
                    self.completed_highlight = None
                    total_rows = float(self.text.index("end-1c"))
                    float_top_rows = self.parent.scrolly.get()[0] * total_rows
                    if float_top_rows == 0.0:
                        float_top_rows = 1.0
                    elif float_top_rows > 10:
                        float_top_rows -= 10
                    elif float_top_rows > 20:
                        float_top_rows -= 20
                    elif float_top_rows > 30:
                        float_top_rows -= 30
                    top_rows = str(float_top_rows).split(".")[0] + ".0"
                    bottom_rows = str(now_bottom_rows * total_rows + 30).split(".")[0] + ".0"
                    data_start = self.text.get(top_rows, bottom_rows)
                    is_line_break = None
                    len_data_start = len(data_start)
                    if len_data_start > 3000:# 字数太多会导致卡顿，超过3000个字符就停止语法高亮
                        self.completed_highlight = True
                        continue
                    elif len_data_start > 1:
                        if data_start[0] == "\n":
                            self.text.insert(top_rows, ' ')#插入一个空字符，防止后面语法高亮时少算一格位置
                            is_line_break = True
                    data = self.text.get(top_rows, bottom_rows)
                    if len(data) > 1:
                        if data[0] == "\n":
                            data = " " + data
                    self.text.mark_set("range_start", top_rows)
                    obj_lex = lex(data, self.lexer)
                    counter = 0
                    for token, content in obj_lex:#这个循环耗时且处理器资源占用较大
                        counter += 1
                        if counter > 3000:
                            break
                        self.text.mark_set("range_end", "range_start + %dc" % len(content))
                        self.text.tag_add(str(token), "range_start", "range_end")
                        self.text.mark_set("range_start", "range_end")

                    if is_line_break:
                        self.text.delete(top_rows, float_top_rows+0.1)
                    self.completed_highlight = True

    def load_new_theme(self, path, *args):
        with open(path) as new_theme_config:
            new_config = load(new_theme_config, Loader=FullLoader)
            self.syntax_and_themes.save_theme_to_config(path)

        self.comment_color = new_config['comment_color']
        self.string_color = new_config['string_color']
        self.number_color = new_config['number_color']
        self.keyword_color = new_config['keyword_color']
        self.operator_color = new_config['operator_color']
        self.bultin_function_color = new_config['bultin_function_color']
        self.class_color = new_config['class_self_color']
        self.namespace_color = new_config['namespace_color']
        self.class_name_color = new_config['class_name_color']
        self.function_name_color = new_config['function_name_color']
        self.text_color = new_config['font_color']
        self.type_color = new_config['type_color']
        self.parent.text_selection_bg_clr = new_config['selection_color']
        self.parent.insertion_color = new_config['font_color']
        self.parent.menu_fg = new_config['menu_fg_active']
        self.parent.menu_bg = new_config['menu_bg_active']
        self.parent.font_color = new_config['font_color']
        self.parent.bg_color = new_config['bg_color']
        self.parent.menubar_bg_active = new_config['menu_bg_active']
        self.parent.menubar_fg_active = new_config['menu_fg_active']
        self.menu_bg = new_config['menu_bg_active']
        self.menu_fg = new_config['menu_fg_active']
        self.parent.reconfigure_settings()
        if not args:#启动时，还未加载脚本前，不需要设置语法高亮
            self.initial_highlight()

    def clear_existing_tags(self):
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)


class Menubar():#菜单栏
    def __init__(self, parent):# 初始化编辑器的菜单栏
        self._parent = parent
        self.syntax = parent.syntax_highlighter
        self.ptrn = r'[^\/]+$'
        font_specs = ('Droid Sans Fallback', 12)

        # 在菜单栏中设置基本功能
        menubar = tk.Menu(
          parent.master,
          font=font_specs,
          fg=parent.menu_fg,
          bg=parent.menu_bg,
          activeforeground= parent.menubar_fg_active,
          activebackground= parent.menubar_bg_active,
          activeborderwidth=0,
          bd=0)

        parent.master.config(menu=menubar)
        self._menubar = menubar
        # 在菜单栏中添加功能文件下拉列表
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(
          label='加载上一个文件',
          accelerator='Ctrl + P',
          command=parent.load_previous_file)
        # 功能 创建新文件
        file_dropdown.add_command(
          label='新建文件',
          accelerator='Ctrl + N',
          command=parent.new_file)
        # 功能 打开文件
        file_dropdown.add_command(
          label='打开文件',
          accelerator='Ctrl + O',
          command=parent.open_file)
        # 功能 打开目录
        file_dropdown.add_command(
          label='打开目录',
          command=parent.open_dir)
        # 功能 保存文件
        file_dropdown.add_command(
          label='保存',
          accelerator='Ctrl + S',
          command=parent.save)
        # 功能 另存为
        file_dropdown.add_command(
          label='另存为',
          accelerator='Ctrl + Shift + S',
          command=parent.save_as)
        # 功能 退出
        file_dropdown.add_separator()
        file_dropdown.add_command(
          label='退出',
          command=parent.on_closing)

        # 下拉菜单 视图
        view_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        view_dropdown.add_command(
          label='隐藏行号',
          accelerator='Ctrl + Shift + L',
          command=parent.toggle_linenumbers)
        view_dropdown.add_command(
          label='关闭语法高亮',
          accelerator='Ctrl + Shift + H',
          command=parent.switch_highlight)
        view_dropdown.add_command(
          label='文字放大',
          accelerator='Ctrl + 鼠标滚轮向上',
          command=parent.change_font_add)
        view_dropdown.add_command(
          label='文字缩小',
          accelerator='Ctrl + 鼠标滚轮向下',
          command=parent.change_font_sub)

        # 下拉菜单 编辑
        edit_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        edit_dropdown.add_command(
          label='注释代码',
          accelerator='Ctrl + E',
          command=parent.code_comment)
        edit_dropdown.add_command(
          label='取消注释',
          accelerator='Ctrl + Q',
          command=parent.code_uncomment)
        edit_dropdown.add_command(
          label='增加缩进',
          accelerator='Tab',
          command=parent.tab_text_add)
        edit_dropdown.add_command(
          label='减小缩进',
          accelerator='Shift + Tab',
          command=parent.tab_text_sub)

        # 菜单 工具
        tools_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        tools_dropdown.add_command(
          label='查询与替换',
          accelerator='Ctrl + F',
          command=parent.show_find_window)
        tools_dropdown.add_command(
          label='显示文件树',
          accelerator='Ctrl + T',
          command=parent.show_file_tree)
        tools_dropdown.add_command(
          label='打开颜色选择器',
          accelerator='Ctrl + M',
          command=self.open_color_picker)

        # 菜单 设置
        label_bootSelfStart='开机自启动'
        if parent.isStartUp():#查询是否开机自启动
            label_bootSelfStart="√ 开机自启动"
        set_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        set_dropdown.add_command(
          label=label_bootSelfStart,
          command=parent.bootSelfStart)

        # 菜单 主题
        theme_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        theme_dropdown.add_command(
          label='黑暗之心',
          command=self.syntax.syntax_and_themes.load_darkheart)
        theme_dropdown.add_command(
          label='德古拉',
          command=self.syntax.syntax_and_themes.load_dracula)
        theme_dropdown.add_command(
          label='荒漠',
          command=self.syntax.syntax_and_themes.load_desert)
        theme_dropdown.add_command(
          label='明亮',
          command=self.syntax.syntax_and_themes.load_githubly)
        theme_dropdown.add_command(
          label='矿箱',
          command=self.syntax.syntax_and_themes.load_gruvbox)
        theme_dropdown.add_command(
          label='材料',
          command=self.syntax.syntax_and_themes.load_material)
        theme_dropdown.add_command(
          label='莫诺凯',
          command=self.syntax.syntax_and_themes.load_monokai)
        theme_dropdown.add_command(
          label='莫诺凯+',
          command=self.syntax.syntax_and_themes.load_monokai_pro)
        theme_dropdown.add_command(
          label='南瓜',
          command=self.syntax.syntax_and_themes.load_pumpkin)
        theme_dropdown.add_command(
          label='铁锈',
          command=self.syntax.syntax_and_themes.load_rust)
        theme_dropdown.add_command(
          label='暗青',
          command=self.syntax.syntax_and_themes.load_solarized)
        theme_dropdown.add_command(
          label='深黑',
          command=self.syntax.syntax_and_themes.load_deepBlack)
        theme_dropdown.add_command(
          label='凯蒂',
          command=self.syntax.syntax_and_themes.load_helloKitty)

        # 菜单 手册
        manual_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        manual_dropdown.add_command(
          label='Lua 教程',
          command=self.open_lua_url)
        manual_dropdown.add_command(
          label='API 手册',
          command=self.open_handbook)

        # 菜单 关于
        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label='免责声明：非盈利项目，仅供学习交流使用')
        about_dropdown.add_command(label='项目地址：www.github.com/1C1T/RedBox',
          command=self.open_github)

        # 菜单栏添加按钮
        menubar.add_cascade(label='文件', menu=file_dropdown)
        menubar.add_cascade(label='视图', menu=view_dropdown)
        menubar.add_cascade(label='编辑', menu=edit_dropdown)
        menubar.add_cascade(label='工具', menu=tools_dropdown)
        menubar.add_cascade(label='设置', menu=set_dropdown)
        menubar.add_cascade(label='主题', menu=theme_dropdown)
        menubar.add_cascade(label='手册', menu=manual_dropdown)
        menubar.add_cascade(label='关于', menu=about_dropdown)

        self.menu_fields = [field for field in (
            file_dropdown, view_dropdown, edit_dropdown, tools_dropdown, set_dropdown, theme_dropdown, manual_dropdown, about_dropdown)]

        # 设置可变子菜单
        self.view_dropdown = view_dropdown
        self.set_dropdown = set_dropdown
        self.theme_dropdown = theme_dropdown

    def reconfigure_settings(self):# 功能 恢复默认设置
        settings = self._parent.loader.load_settings_data()
        for field in self.menu_fields:
            field.configure(
                bg=self._parent.menu_bg,
                fg=self._parent.menu_fg,
                activeforeground=self._parent.menubar_fg_active,
                activebackground=self._parent.menubar_bg_active,
                background = self._parent.bg_color,
            )

        self._menubar.configure(
            bg=self._parent.menu_bg,
            fg=self._parent.menu_fg,
            background = self._parent.bg_color,
            activeforeground= self._parent.menubar_fg_active,
            activebackground = self._parent.menubar_bg_active,
          )

    def open_color_picker(self):# 可以在此处设置不同文本类型的颜色
        return askcolor(title='颜色菜单', initialcolor='#d5c4a1')[1]

    def hide_menu(self):# 隐藏菜单栏
        self._parent.master.config(menu='')

    def show_menu(self):# 显示菜单栏
        self._parent.master.config(menu=self._menubar)

    def open_lua_url(self): # 打开lua官方教程网站
        try:
            if os.path.exists("./docs_lua.url") == False:# lua官方教程链接
                with open("./docs_lua.url", "w", encoding="utf-8") as file:
                    file.write("[InternetShortcut]\nURL=https://www.lua.org/manual/5.1/\n")
            if os.path.exists("./docs_lua.url") == True:
                os.startfile(".\docs_lua.url")
        except Exception as e:
            pass

    def open_handbook(self): # 打开API手册
        try:
            if os.path.exists("./API 参考文档.docx") == True:
                os.startfile(".\API 参考文档.docx")
        except Exception as e:
            pass

    def open_github(self): # 打开github项目地址
        try:
            if os.path.exists("./github.url") == False:# lua官方教程链接
                with open("./github.url", "w", encoding="utf-8") as file:
                    file.write("[InternetShortcut]\nURL=https://github.com/1C1T/RedBox/\n")
            if os.path.exists("./github.url") == True:
                os.startfile(".\github.url")
        except Exception as e:
            pass


class Statusbar:#状态栏
    def __init__(self, parent):# 初始化状态栏
        self._parent = parent
        self.save_bg = '#FF6859'
        self.status_fg = '#000000'
        self.error_bg = '#B00020'
        self.hint_bg = '#B15DFF'
        # 设置状态栏
        font_specs = ('Droid Sans Fallback', 10)

        self.status = tk.StringVar()

        label = tk.Label(
            parent.textarea,
            textvariable=self.status,
            fg=parent.font_color,
            bg='#fff',
            anchor='se',
            font=font_specs)
        
        self._label = label

    def update_status(self, event):# 状态栏状态更新
        if event == 'saved':
            self.display_status_message('更改已保存', msg_type='save')
        elif event == 'no file':
            self.display_status_message('未检测到文件. 请创建或打开文件', msg_type='error')
        elif event == 'created':
            self.display_status_message('文件已创建', msg_type='hint')
        else:
            self.hide_status_bar()

    def display_status_message(self, message, msg_type='error'):
        self.show_status_bar()
        self.status.set(message)
        if msg_type == 'save':
            self.save_color()
        elif msg_type == 'hint':
            self.hint_color()
        else:
            self.error_color()

    def error_color(self):
        self._label.config(bg=self.error_bg, fg=self.status_fg)

    def save_color(self):
        self._label.config(bg=self.save_bg, fg=self.status_fg)

    def hint_color(self):
        self._label.config(bg=self.hint_bg, fg=self.status_fg)

    def hide_status_bar(self):# 隐藏状态栏
        self._label.pack_forget()

    def show_status_bar(self):# 显示状态栏
        self._label.pack(side=tk.BOTTOM)

    def reconfigure_status_label(self):
        self._label.config()


class TextLineNumbers(tk.Canvas):# 行号
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self._text_font = parent.settings['font_family']
        self._parent = parent
        self.textwidget = parent.textarea
        self.completed_redraw = True

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        if not self.visible:
            return
        if not self.completed_redraw:
            return
        self.completed_redraw = None
        font_color = self._parent.menu_fg
        bg_color = self._parent.bg_color
        indicator_on = self._parent.current_line_indicator
        current_line_symbol = self._parent.current_line_symbol

        self.delete('all')
        self.config(bd=0, bg=bg_color, highlightthickness=0)

        i = self.textwidget.index('@0,0')
        linenum = ''
        while True:
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            index = self.textwidget.index(tk.INSERT)
            pos = index.split('.')[0]
            if float(i) >= 10:
                linenum = str(i).split('.')[0]
                if pos == linenum and indicator_on:
                    linenum = linenum + current_line_symbol
            else:
                linenum = ' ' + str(i).split('.')[0]
                if ' ' + pos == linenum and indicator_on:
                    linenum = linenum + current_line_symbol
            self.create_text(5, y, anchor='nw',
                             text=linenum,
                             font=(self._text_font, self._parent.font_size),
                             fill=font_color)
            i = self.textwidget.index('%s+1line' % i)
        int_linenum = int(linenum)
        if int_linenum < 1000:
            self.config(width=(self._parent.font_size * 3))
        elif int_linenum < 10000:
            self.config(width=(self._parent.font_size * 4))
        elif int_linenum < 100000:
            self.config(width=(self._parent.font_size * 5))
        elif int_linenum < 1000000:
            self.config(width=(self._parent.font_size * 6))
        elif int_linenum < 10000000:
            self.config(width=(self._parent.font_size * 7))
        else:
            self.config(width=(self._parent.font_size * 8))
        self.completed_redraw = True

    @property
    def visible(self):
        return self.cget('state') == 'normal'

    @visible.setter
    def visible(self, visible):
        self.config(state='normal' if visible else 'disabled')

        if visible:
            self.redraw()
            self._parent.menubar.view_dropdown.entryconfig(0, label="隐藏行号")
        else:
            self.delete('all')
            self.config(width=0)
            self._parent.menubar.view_dropdown.entryconfig(0, label="显示行号")


class CustomText(tk.Text):#自定义文本
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # 为底层小部件创建代理
        self.bg_color ='#eb4034'
        self.fg_color = '#eb4034'
        self.active_fg = '#eb4034'
        self.active_bg = '#eb4034'
        self.isControlPressed = False
        self._orig = self._w + '_orig'
        self.tk.call('rename', self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # 让实际的小部件执行请求的操作
        try:
            cmd = (self._orig,) + args
            result = ''
            if not self.isControlPressed:
                # 如果命令不存在，则执行事件
                result = self.tk.call(cmd)
            else:
                # 按下 Ctrl 时抑制 y滚动条 和 x滚动条
                if args[0:2] not in [('yview', 'scroll'), ('xview', 'scroll')]:
                    result = self.tk.call(cmd)
        except tk.TclError:
            result = ''

        # 如果添加或删除某些内容，则生成一个事件，或者光标位置改变
        if (args[0] in ('insert', 'replace', 'delete') or 
            args[0:3] == ('mark', 'set', 'insert') or
            args[0:2] == ('xview', 'moveto') or
            args[0:2] == ('xview', 'scroll') or
            args[0:2] == ('yview', 'moveto') or
            args[0:2] == ('yview', 'scroll')
        ):
            self.event_generate('<<Change>>', when='tail')

        # 返回实际小部件返回的内容
        return result

    def find(self, text_to_find):
        length = tk.IntVar()
        index = self.search(
            text_to_find,
            self.find_search_starting_index,
            stopindex=tk.END, count=length)

        if index:
            self.tag_remove('find_match', 1.0, tk.END)

            end = f'{index}+{length.get()}c'
            self.tag_add('find_match', index, end)
            self.see(index)

            self.find_search_starting_index = end
            self.find_match_index = index
        else:
            if self.find_match_index != 1.0:
                if tk.messagebox.askyesno("没有更多结果", "向下没有匹配结果。是否从头开始匹配?"):
                    self.find_search_starting_index = 1.0
                    self.find_match_index = None
                    return self.find(text_to_find)
            else:
                tk.messagebox.showinfo("匹配失败", "没有找到匹配的文本")

    def replace_text(self, target, replacement):
        if self.find_match_index:
            current_found_index_line = str(self.find_match_index).split('.')[0]

            end = f"{self.find_match_index}+{len(target)}c"
            self.replace(self.find_match_index, end, replacement)

            self.find_search_starting_index = current_found_index_line + '.0'

    def cancel_find(self):
        self.find_search_starting_index = 1.0
        self.find_match_index = None
        self.tag_remove('find_match', 1.0, tk.END)

    def reload_text_settings(self):
        self.bg_color = '#eb4034'
        self.fg_color = '#eb4034'
        self.active_fg = '#eb4034'
        self.active_bg = '#eb4034'


class ConsoleText(tk.Text):#控制台
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        self.stdoutbak = sys.stdout
        sys.stdout = self

    def write(self, info):
        # info信息即标准输出sys.stdout和sys.stderr接收到的输出信息
        if info == "__ClearLog__":
            self.configure(state="normal")
            self.delete(1.0, tk.END)
            self.configure(state="disabled")
        else:
            self.configure(state="normal")
            self.insert('end', info)	# 在多行文本控件最后一行插入print信息
            self.update()	# 更新显示的文本，不加这句插入的信息无法显示
            self.see(tk.END)	# 始终显示最后一行，不加这句，当文本溢出控件最后一行时，不会自动显示最后一行
            self.configure(state="disabled")

    def restoreStd(self):
        # 恢复标准输出
        sys.stdout = self.stdoutbak


class FindWindow(tk.Toplevel):#搜索与替换
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.loader = QuietLoaders()
        windows_x = int((self.winfo_screenwidth()-260)/2)  # 窗口左上角x坐标
        windows_y = int((self.winfo_screenheight()-100)/2) # 窗口左上角y坐标
        self.geometry(f'260x100+{windows_x}+{windows_y}')  # 设置窗口尺寸，并使窗口屏幕置中
        self.resizable(width=False, height=False)          # 设置窗口的宽、高：不可变
        self.icon_path = self.loader.resource_path(
            os.path.join('data', 'RedBox.png'))
        self.icon = tk.PhotoImage(file=self.icon_path)
        self.iconphoto(False, self.icon)
        self.title('搜索与替换')
        self.transient(master)
        self.configure(bg=master.bg_color)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.bg_color = master.bg_color
        self.fg_color = master.fg_color
        self.active_fg = master.active_fg
        self.active_bg = master.active_bg

        self.text_to_find = tk.StringVar()
        self.text_to_replace_with = tk.StringVar()

        top_frame = tk.Frame(self, bg=self.bg_color)
        middle_frame = tk.Frame(self, bg=self.bg_color)
        bottom_frame = tk.Frame(self, bg=self.bg_color)

        self.style.configure(
            'editor.TLabel',
             background=self.bg_color,
             foreground='#fff',)

        find_entry_label = ttk.Label(top_frame, text="搜索: ", style="editor.TLabel")
        self.find_entry = ttk.Entry(top_frame, textvar=self.text_to_find)

        replace_entry_label = ttk.Label(middle_frame, text="替换: ", style="editor.TLabel")
        self.replace_entry = ttk.Entry(middle_frame, textvar=self.text_to_replace_with)

        self.style.configure('editor.TButton',
                background=self.bg_color,
                foreground='#fff',
                activeforeground=self.active_fg)

        self.style.map('editor.TButton',
                background=[('pressed', self.active_fg), ('active', self.active_bg)])

        self.find_button = ttk.Button(bottom_frame, text="搜索", command=self.on_find, style="editor.TButton")
        self.replace_button = ttk.Button(bottom_frame, text="替换", command=self.on_replace, style="editor.TButton")
        self.cancel_button = ttk.Button(bottom_frame, text="取消", command=self.on_cancel, style="editor.TButton")

        find_entry_label.pack(side=tk.LEFT, padx=(5, 12))
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=(0, 5))

        replace_entry_label.pack(side=tk.LEFT, padx=(5, 12))
        self.replace_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=(0, 5))

        self.find_button.pack(side=tk.LEFT, padx=(5, 0))
        self.replace_button.pack(side=tk.LEFT, padx=(5, 0))
        self.cancel_button.pack(side=tk.LEFT, padx=(5, 5))

        top_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=0)
        middle_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=0)
        bottom_frame.pack(side=tk.TOP, expand=1, fill=tk.X)

        self.find_entry.focus_force()

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def on_find(self):
        self.master.find(self.text_to_find.get())

    def on_replace(self):
        self.master.replace_text(self.text_to_find.get(), self.text_to_replace_with.get())

    def on_cancel(self):
        self.master.cancel_find()
        self.destroy()


class ContextMenu(tk.Listbox):#右键菜单
    def __init__(self, parent, *args, **kwargs):# 初始化函数
        tk.Listbox.__init__(self, parent, *args, **kwargs)

        self.font_family = parent.font_family
        self.font_color = parent.menu_fg
        self.bg_color = parent.bg_color
        self.active_bg = parent.menubar_bg_active
        self.active_fg = parent.menubar_fg_active
        self.parent = parent

        self.changes = [""]
        self.steps = int()

        # 设置 tk.右键单击菜单栏
        self.right_click_menu = tk.Menu(
            parent,
            font='DroidSansFallback',
            fg=self.font_color,
            bg=self.bg_color,
            activebackground=self.active_bg,
            activeforeground=self.active_fg,
            bd=0,
            tearoff=0)

        self.right_click_menu.add_command(
            label='加粗',
            command=self.bold)

        self.right_click_menu.add_command(
            label='高亮',
            command=self.hightlight)

    def popup(self, event):
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.right_click_menu.grab_release()

    def undo(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            self.parent.textarea.delete(0, tk.END)
            self.parent.textarea.insert(tk.END, self.changes[self.steps])

    def redo(self, event=None):
        if self.steps < len(self.changes):
            self.parent.textarea.delete(0, tk.END)
            self.parent.textarea.insert(tk.END, self.changes[self.steps])
            self.steps += 1

    def add_changes(self, event=None):
        if self.parent.textarea.get() != self.changes[-1]:
            self.changes.append(self.parent.textarea.get())
            self.steps += 1

    def bold(self, event=None):# 将所选文本设置为粗体
        if self.parent.filename:
            try:
                current_tags = self.parent.textarea.tag_names("sel.first")
                bold_font = tk_font.Font(self.parent.textarea, self.parent.textarea.cget("font"))
                bold_font.configure(weight = "bold")
                self.parent.textarea.tag_config("bold", font = bold_font)
                if "bold" in current_tags:
                    self.parent.textarea.tag_remove("bold", "sel.first", "sel.last")
                else:
                    self.parent.textarea.tag_add("bold", "sel.first", "sel.last")
            except tk.TclError:
                pass
        else:
            self.parent.statusbar.update_status('no file')

    def hightlight(self, event=None):
        if self.parent.filename:
            try:
                # 释放ctrl键
                self.parent.control_key = False
                new_color = self.parent.menubar.open_color_picker()
                current_tags = self.parent.textarea.tag_names("sel.first")
                highlight_font = tk_font.Font(self.parent.textarea, self.parent.textarea.cget("font"))
                self.parent.textarea.tag_config(
                    f"highlight_{new_color}",
                    font = highlight_font,
                    foreground = "black",
                    background = new_color)
                if "highlight" in current_tags:
                    for tag in current_tags:
                        if "highlight" in tag:
                            self.parent.textarea.tag_remove(tag, "sel.first", "sel.last")
                else:
                    self.parent.textarea.tag_add("highlight", "sel.first", "sel.last")
                    self.parent.textarea.tag_add(f"highlight_{new_color}","sel.first", "sel.last")
            except tk.TclError:
                pass
        else:
            self.parent.statusbar.update_status('no file')


class QuietLoaders:#设置加载
    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

    def __init__(self):
        self.settings_path = self.resource_path(os.path.join('data', 'config/settings.yaml'))
        self.default_settings_path = self.resource_path(os.path.join('data', 'config/settings-default.yaml'))

    def load_settings_data(self, default=False):
        if not default:
            with open(self.settings_path, 'r', encoding="gbk") as some_config:
                return load(some_config, Loader=FullLoader)
        else:
            with open(self.default_settings_path, 'r', encoding="gbk") as some_config:
                return load(some_config, Loader=FullLoader)

    def store_settings_data(self, new_settings):
        with open(self.settings_path, 'w') as settings_config:
            dump(new_settings, settings_config)


class FileTree(tk.Toplevel):#文件树
    def __init__(self, master, **kwargs):
        tk.Toplevel.__init__(
            self,
            bd=0,
            bg=master.bg_color,# 背景颜色似乎不能改变
            highlightbackground=master.bg_color)
        self.iconphoto(False, master.icon)
        self.master = master
        self.font_specs = ('Droid Sans Fallback', 12)
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.style.configure(
            'Treeview',
            font=self.font_specs,
            foreground=master.menu_fg,
            background=master.bg_color,
            fieldbackground=master.bg_color,
            highlightthickness=0,
            bd=0)
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # 移除边框
        windows_x = int((self.winfo_screenwidth()-200)/2)  # 窗口左上角x坐标
        windows_y = int((self.winfo_screenheight()-400)/2) # 窗口左上角y坐标
        self.geometry(f'200x400+{windows_x}+{windows_y}')  # 设置窗口尺寸，并使窗口屏幕置中
        self.title('脚本目录')
        self.transient(master)
        self.tree=ttk.Treeview(
            self,
            height=20,
            selectmode='browse',
            show='tree',
            style='Treeview')
        self.minsize(200,125)
        self.maxsize(1000, 1000)
        
        # 这在某种程度上是有效的。可能有更好的方法来搜索文件系统。
        def folder_mania(path, location=""):
            starting_content = ''
            try:
                starting_content = os.listdir(master.dirname)
            except (NotADirectoryError, FileNotFoundError, PermissionError) as e:
                print(e)
            if path == master.dirname:
                location = ""
                files = [file for file in starting_content if '.' in file]
                folders = [folder for folder in starting_content if '.' not in folder]
            else:
                new_content = os.listdir(path)
                files = [file for file in new_content if '.' in file]
                folders = [folder for folder in new_content if '.' not in folder]
            summ = 0
            for count, folder in enumerate(folders, 1):
                if folder:
                    folder_name=self.tree.insert(location, count, text=folder, values=[folder])
                    new_path = path + '/' + folder
                    try:
                        if len(os.listdir(new_path)) > 0:
                            folder_mania(new_path, location=folder_name)
                    except (NotADirectoryError, FileNotFoundError):
                        pass
                    except PermissionError as e:
                        print(e)
                        break
            for count, file in enumerate(files, 1):
                adjusted_count = count + summ
                if adjusted_count % 2 == 0:
                    tag = 'odd'
                else:
                    tag = 'even'
                self.tree.insert(location, adjusted_count, text=file, tags=(tag,), values=[location])
            summ += 1

        folder_mania(master.dirname)
        self.tree_bindings()
        self.tree.pack(side=tk.TOP,fill=tk.BOTH)

    def OnDoubleClick(self, event):
        self.master.filename = self.master.dirname
        item = self.tree.identify("item", event.x, event.y)
        folder_id = self.tree.parent(item)
        folder = ''
        while True:
            try:
                folder_path = self.tree.item(folder_id)["values"][0]
                folder = folder_path + '/' + folder
                folder_id = self.tree.parent(folder_id)
            except IndexError:
                break
        filename = self.tree.item(item)["text"]
        file_path = folder + filename if folder else filename
        if '.' in file_path:
            try:
                self.master.filename += '/' + file_path
                self.master.textarea.delete(1.0, tk.END)
                self.master.clear_and_replace_textarea()
            except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
                self.master.filename = os.getcwd()
        self.master.set_window_title(self.master.filename)

    def tree_bindings(self):
        self.tree.bind('<Double-Button-1>', self.OnDoubleClick)


class RedBox(tk.Frame):#主类 红盒窗口
    def __init__(self, *args, **kwargs):
        #将整个过程组合在一起的主类
        tk.Frame.__init__(self, *args, **kwargs)
        # 开机自启后隐藏界面
        if len(sys.argv) > 1:
            if sys.argv[1] == '-startup':
                master.withdraw()
                # 修改当前工作目录
                exe_name = sys.executable.split('\\')[-1]
                os.chdir(sys.executable.split(exe_name)[0])
        # 定义编辑器窗口的大小
        windows_x = int((self.winfo_screenwidth()-1280)/2)  # 窗口左上角x坐标
        windows_y = int((self.winfo_screenheight()-720)/2) # 窗口左上角y坐标
        master.geometry(f'1280x720+{windows_x}+{windows_y}')  # 设置窗口尺寸，并使窗口屏幕置中
        self.configure(bg='black')
        self.loader = QuietLoaders()
        self.icon_path = self.loader.resource_path(os.path.join('data', 'RedBox.png'))
        self.icon = tk.PhotoImage(file = self.icon_path)
        master.iconphoto(False, self.icon)

        # 根据settings.yaml中定义的设置启动编辑器
        self.settings = self.loader.load_settings_data()

        # 可编辑的设置变量
        self.browser = self.settings['web_browser']
        self.font_family = self.settings['font_family']
        self.tab_size = self.settings['tab_size']
        self.font_size = int(self.settings['font_size'])
        self.top_spacing = self.settings['text_top_lineheight']
        self.bottom_spacing = self.settings['text_bottom_lineheight']
        self.padding_x = self.settings['textarea_padding_x']
        self.padding_y = self.settings['textarea_padding_y']
        self.insertion_blink = 300
        self.tab_size_spaces = self.settings['tab_size']
        self.text_wrap = self.settings['text_wrap']
        self.autoclose_parentheses = self.settings['autoclose_parentheses']
        self.autoclose_curlybraces = self.settings['autoclose_curlybraces']
        self.autoclose_squarebrackets = self.settings['autoclose_squarebrackets']
        self.autoclose_singlequotes = self.settings['autoclose_singlequotes']
        self.autoclose_doublequotes = self.settings['autoclose_doublequotes']
        self.scrollx_width = self.settings['horizontal_scrollbar_width']
        self.scrolly_width = self.settings['vertical_scrollbar_width']
        self.current_line_symbol = self.settings['current_line_indicator_symbol']
        self.current_line_indicator = self.settings['current_line_indicator']
        self.border = self.settings['textarea_border']

        # 编辑配色方案变量
        self.insertion_color = '#eb4034'
        self.bg_color = '#eb4034'
        self.font_color = '#eb4034'
        self.text_selection_bg_clr = '#eb4034'
        self.scrollx_clr = '#242222'
        self.troughx_clr = '#242222'
        self.scrollx_active_bg = '#423d3d'
        self.scrolly_clr = '#242222'
        self.troughy_clr = '#242222'
        self.scrolly_active_bg = '#423d3d'
        self.menubar_bg_active = '#eb4034'
        self.menubar_fg_active = '#eb4034'
        self.menu_fg = '#eb4034'
        self.menu_bg = '#eb4034'

        # 文件对话框文本颜色的配置
        self.font_style = tk_font.Font(family=self.font_family,
                                       size=self.font_size)

        font_size_consoleText = self.font_size - 3
        if font_size_consoleText < 3:
            font_size_consoleText = 3
        font_style_consoleText = tk_font.Font(family="宋体",
                                       size=font_size_consoleText)

        self.italics = tk_font.Font(family=self.font_family, slant='italic', size=self.font_size)
        self.bold = tk_font.Font(family=self.font_family, weight='bold', size=self.font_size)
        self.header1 = tk_font.Font(family=self.font_family, weight='bold', size=self.font_size + 15)
        self.header2 = tk_font.Font(family=self.font_family, weight='bold', size=self.font_size + 7)

        self.filename = self.get_script_path()
        self.previous_file = self.filename
        master.title(f'{self.filename} - 红盒')
        self.master = master
        self.dirname = "脚本"
        self.textarea = CustomText(self)
        self.consoleText = ConsoleText(self)

        # 设置滚动条的风格
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Vertical.TScrollbar", 
            background=self.font_color, darkcolor=self.font_color, lightcolor=self.font_color,
            troughcolor=self.bg_color, arrowcolor=self.bg_color, sliderlength=16)

        self.style.configure("Horizontal.TScrollbar", 
            background=self.font_color, darkcolor=self.font_color, lightcolor=self.font_color,
            troughcolor=self.bg_color, arrowcolor=self.bg_color, sliderlength=16)

        self.scrolly = ttk.Scrollbar(
            master,
            command=self.textarea.yview,
            orient='vertical')

        self.scrollx = ttk.Scrollbar(
            master,
            command=self.textarea.xview,
            orient='horizontal')

        self.textarea.configure(
            yscrollcommand=self.scrolly.set,
            xscrollcommand=self.scrollx.set,
            bg=self.bg_color,
            fg=self.font_color,
            wrap=self.text_wrap,# "none" 不换行
            spacing1=self.top_spacing, 
            spacing3=self.bottom_spacing,
            selectbackground= self.text_selection_bg_clr,
            insertbackground=self.insertion_color,
            insertofftime=self.insertion_blink,
            bd=self.border,
            highlightthickness=0,
            highlightbackground='black',
            font=self.font_style,
            undo=True,
            autoseparators=True,
            maxundo=-1,
            padx=self.padding_x,
            pady=self.padding_y)

        self.consoleText.configure(
            bg=self.bg_color,
            fg=self.font_color,
            font=font_style_consoleText,
            wrap="char",# "char" 自动换行
            height=7,
            bd=0,
            spacing1=self.top_spacing, 
            spacing3=self.bottom_spacing,
            padx=self.padding_x,
            pady=self.padding_y)

        self.initial_content = self.textarea.get("1.0", tk.END)

        # 从文本区域检索字体并设置制表符宽度
        self._font = tk_font.Font(font=self.textarea['font'])
        self._tab_width = self._font.measure(' ' * self.tab_size_spaces)
        self.textarea.config(tabs=(self._tab_width,))

        self.context_menu = ContextMenu(self)
        self.linenumbers = TextLineNumbers(self)
        self.syntax_highlighter = SyntaxHighlighting(self, self.textarea, self.initial_content)
        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        self.syntax_highlighter.syntax_and_themes.load_theme_from_config()# 加载主题

        self.linenumbers.attach(self.textarea)
        self.consoleText.pack(side=tk.BOTTOM, fill=tk.X)
        self.scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.textarea.pack(side=tk.RIGHT, fill='both', expand=True)
        
        self.textarea.find_match_index = None
        self.textarea.find_search_starting_index = 1.0

        # 调用函数绑定热键
        self.bind_shortcuts()
        self.control_key = False
        self.menu_hidden = False
        self.textEdited = False
        self.total_word = 0

        # 加载脚本文件
        self.clear_and_replace_textarea()

        # 创建托盘图标
        self.image = Image.open("data/RedBox.png")  # 自定义图标图片
        self.menu = (
            pystray.MenuItem(text="图标", action=self.restore_window, default=True, visible=False),
            pystray.MenuItem(text="打开", action=self.restore_window),
            pystray.MenuItem(text="退出", action=self.exit_application)
        )
        self.tray_icon = pystray.Icon("name", self.image, "红盒\n版本号：1.0", self.menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

        # 链接winmm动态库 设置sleep精度为1毫秒
        ctypes.windll.LoadLibrary('winmm').timeBeginPeriod(1)
        # 主窗口运行
        tk.Frame.pack(self, side='top', fill='both', expand=True)
        self.master.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.master.mainloop()

    def get_script_path(self):#获取上次最后加载的脚本路径
        last_path = ""
        if os.path.exists("脚本/script_path"):
            with open("脚本/script_path", "r+", encoding = "utf-8") as file:
                last_path = file.readline()
                #如果script_path文件里面的脚本路径不正确，则设置一个默认路径
                if not os.path.exists(last_path):
                    last_path = os.getcwd()
                    file.truncate(0)#清空文件内容
                    file.seek(0)
                    file.write(last_path)
        else:
            last_path = os.getcwd()
        return last_path

    def save_script_path(self):#保存脚本路径
        with open("脚本/script_path", "w", encoding = "utf-8") as file:
            file.write(self.filename)

    def create_new_script(self):#创建新脚本
        # 删除当前区域中的所有文本并将窗口标题设置为默认值
        #如果用快捷键打开时，ctrl键状态为None，则不执行后续代码
        self.textarea.delete(1.0, tk.END)
        script_path = os.path.abspath("./脚本")
        newFile = script_path + "\新脚本.lua"
        if not os.path.exists(newFile):# 如果不存在则创建
            with open(newFile, 'w', encoding="utf-8") as f:
                pass
        try:
            previous = newFile
            self.filename = newFile
            self.previous_file = previous
            self.set_window_title(name=newFile)
            with open(self.filename, 'r', encoding="utf-8") as f:
                self.textarea.insert(1.0, f.read())
            self.syntax_highlighter.initial_highlight()
            self.updateScript()
            self.save_script_path()#保存脚本路径
        except PermissionError as e:
            print(e)

    def clear_and_replace_textarea(self):# 打开脚本文件
        self.textarea.delete(1.0, tk.END)
        try:
            if not self.filename.endswith(".lua"):# 不是.lua结尾则新建脚本
                self.create_new_script()
                return
            if self.filename:
                with open(self.filename, 'r', encoding="utf-8") as f:
                    self.textarea.insert(1.0, f.read())
        except TypeError as e:
            print("类型错误：", e)
        except Exception as e:
            if self.filename:
                with open(self.filename, 'r', encoding="gbk") as f:
                    self.textarea.insert(1.0, f.read())
        self.syntax_highlighter.initial_highlight()
        self.updateScript()

    def set_new_tab_width(self, tab_spaces = 'default'):# 根据变化重新配置标签宽度
        if tab_spaces == 'default':
            space_count = self.tab_size_spaces
        else:
            space_count = tab_spaces
        _font = tk_font.Font(font=self.textarea['font'])
        _tab_width = _font.measure(' ' * int(space_count))
        self.textarea.config(tabs=(_tab_width,))

    def reconfigure_settings(self, overwrite_with_default=False):# 更改编辑器基本设置
        # 用于在用户更改 settings.yaml 后重新加载设置的函数
        if overwrite_with_default:
            _settings = self.loader.load_settings_data(default=True)
        else:
            _settings = self.loader.load_settings_data()
        font_family = _settings['font_family']
        top_spacing = _settings['text_top_lineheight']
        bottom_spacing = _settings['text_bottom_lineheight']
        insertion_blink = 300
        tab_size_spaces = _settings['tab_size']
        font_size = int(self.settings['font_size'])
        padding_x = _settings['textarea_padding_x']
        padding_y = _settings['textarea_padding_y']
        text_wrap = _settings['text_wrap']
        border = _settings['textarea_border']
        scrollx_width = _settings['horizontal_scrollbar_width']
        scrolly_width = _settings['vertical_scrollbar_width']
        self.autoclose_parentheses = _settings['autoclose_parentheses']
        self.autoclose_curlybraces = _settings['autoclose_curlybraces']
        self.autoclose_squarebrackets = _settings['autoclose_squarebrackets']
        self.autoclose_singlequotes = _settings['autoclose_singlequotes']
        self.autoclose_doublequotes = _settings['autoclose_doublequotes']
        self.linenumbers.current_line_symbol = _settings['current_line_indicator_symbol']
        self.linenumbers.indicator_on = _settings['current_line_indicator']
        self.browser = _settings['web_browser']
        self.textarea.reload_text_settings()
        self.set_new_tab_width(tab_size_spaces)
        self.menubar.reconfigure_settings()
        self.linenumbers._text_font = font_family
        self.linenumbers.redraw()

        font_style = tk_font.Font(family=font_family,
                                  size=font_size)

        font_size_consoleText = font_size - 3
        if font_size_consoleText < 3:
            font_size_consoleText = 3
        font_style_consoleText = tk_font.Font(family="宋体",
                                       size=font_size_consoleText)

        self.menubar._menubar.configure(
            fg=self.menu_fg,
            bg=self.menu_bg,
            activeforeground=self.menubar_fg_active,
            activebackground=self.menubar_bg_active,
            activeborderwidth=0,
            bd=0)

        self.context_menu.right_click_menu.configure(
            font=font_family,
            fg=self.menu_fg,
            bg=self.bg_color,
            activebackground=self.menubar_bg_active,
            activeforeground=self.menubar_fg_active,
            bd=0,
            tearoff=0)
        
        self.style.configure("Vertical.TScrollbar", 
            background=self.font_color, darkcolor=self.font_color, lightcolor=self.font_color,
            troughcolor=self.bg_color, arrowcolor=self.bg_color)

        self.style.configure("Horizontal.TScrollbar", 
            background=self.font_color, darkcolor=self.font_color, lightcolor=self.font_color,
            troughcolor=self.bg_color, arrowcolor=self.bg_color)

        self.textarea.configure(
            font=font_style,
            bg=self.bg_color,
            pady=padding_y,
            padx=padding_x,
            fg=self.font_color,
            spacing1=top_spacing,
            spacing3=bottom_spacing,
            insertbackground=self.insertion_color,
            selectbackground= self.text_selection_bg_clr,
            insertofftime=insertion_blink,
            bd=border,
            highlightthickness=0,
            wrap=text_wrap)

        self.consoleText.configure(
            bg=self.bg_color,
            fg=self.font_color,
            wrap="char",
            font=font_style_consoleText,
            height=7,
            bd=0,
            spacing1=self.top_spacing, 
            spacing3=self.bottom_spacing,
            padx=self.padding_x,
            pady=self.padding_y)

        if overwrite_with_default:
            MsgBox = tk.messagebox.askquestion(
                '重新设置?',
                '您确定要恢复编辑器默认设置吗？',
                icon='warning')
            if MsgBox == 'yes':
                self.loader.store_settings_data(_settings)
            else:
                if self.filename == self.loader.settings_path: 
                    self.save(self.loader.settings_path)
                self.reconfigure_settings()

    def hide_status_bar(self, *args):# 隐藏文本类的状态栏，以便可以在菜单类中使用
        self.statusbar.hide_status_bar()

    def isStartUp(self):#判断是否存在系统启动项中
        isStartUp = False
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey) as reg_key:
            num_values = winreg.QueryInfoKey(reg_key)[1]
            for i in range(num_values):
                value_name, value, value_type = winreg.EnumValue(reg_key, i)
                if value_name == "RedBox":
                    isStartUp = True
        return isStartUp

    def bootSelfStart(self):# 开机自启
        isStartUp = self.isStartUp()
        redboxPath = os.path.abspath("./红盒.exe")
        if isStartUp:#已存在就删除启动项
            subprocess.Popen('reg delete HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v RedBox /f', shell=True, stdin=-1, stdout=-1, stderr=-1)
            self.menubar.set_dropdown.entryconfig(0, label="开机自启动")
        else:
            subprocess.Popen('reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v RedBox /t REG_SZ /d {}" -startup" /f'.format(redboxPath), shell=True, stdin=-1, stdout=-1, stderr=-1)
            self.menubar.set_dropdown.entryconfig(0, label="√ 开机自启动")

    def toggle_linenumbers(self, *args):# 切换行号的可见性
        self.linenumbers.visible = not self.linenumbers.visible

    def set_window_title(self, name=None):# 设置编辑器标题
        # 将窗口标题栏重命名为当前文件的名称
        if name:
            self.master.title(f'{name} - 红盒')
        else:
            self.master.title('无标题 - 红盒')

    def load_previous_file(self, *args):# 加载上一个文件
        if self.previous_file:
            try:
                previous = self.filename
                self.filename = self.previous_file
                self.previous_file = previous
                self.set_window_title(name=self.filename)
                self.textarea.delete(1.0, tk.END)
                self.clear_and_replace_textarea()
            except PermissionError as e:
                print(e)

    def new_file(self, *args):#创建新文件
        # 删除当前区域中的所有文本并将窗口标题设置为默认值
        #如果用快捷键打开时，ctrl键状态为None，则不执行后续代码
        if args and not self.control_key:
            return
        # 释放ctrl键
        self.control_key = False
        self.textarea.delete(1.0, tk.END)
        try:
            newFile = filedialog.asksaveasfilename(
                parent=self.master,
                title='新建文件',
                initialdir=self.dirname,
                initialfile='新建文件.lua',
                filetypes=[('Lua Scripts', '*.lua'),])
            if newFile == '':
                return
            self.previous_file = self.filename
            self.filename = newFile
            textarea_content = self.textarea.get(1.0, tk.END)
            self.set_window_title('新建文件')
            with open(newFile, 'w', encoding="utf-8") as f:
                f.write(textarea_content)
            self.set_window_title(self.filename)
            self.statusbar.update_status('created')
            self.clear_and_replace_textarea()
            self.save_script_path()#保存脚本路径
        except Exception as e:
            print(e)

    def clear_text_tags(self):#清除text的tag
        self.syntax_highlighter.auto_highlight = not self.syntax_highlighter.auto_highlight
        time.sleep(0.5)
        if not self.syntax_highlighter.auto_highlight:
            for tag in self.textarea.tag_names():
                self.textarea.tag_delete(tag)
            self.menubar.view_dropdown.entryconfig(1, label="启用语法高亮")
        else:
            self.syntax_highlighter.initial_highlight()
            self.menubar.view_dropdown.entryconfig(1, label="关闭语法高亮")

    def switch_highlight(self, *args):#切换高亮显示, 默认开启
        threading.Thread(target=self.clear_text_tags).start()# 清除text的tag 并修改窗口子菜单

    def open_file(self, *args):# 在编辑器中打开现有文件
        #如果用快捷键打开时，ctrl键状态为None，则不执行后续代码
        if args and not self.control_key:
            return
        # 释放ctrl键
        self.control_key = False
        # 编辑器可以支持的各种文件类型
        self.previous_file = self.filename
        try:
            openFile = filedialog.askopenfilename(
                parent=self.master,
                initialdir=self.dirname,
                filetypes=[('Lua Scripts', '*.lua'),])
            if openFile == '':
                return
            self.textarea.delete(1.0, tk.END)
            self.filename = openFile
            self.clear_and_replace_textarea()
            if not self.filename:
                self.filename = self.previous_file
            self.set_window_title(name=self.filename)
            self.save_script_path()#保存脚本路径
        except Exception as e:
            print(e)

    def open_dir(self):#打开目录
        try:
            self.dirname = filedialog.askdirectory(
                parent=self.master)
            self.filename = self.dirname
            if self.dirname:
                self.set_window_title(name=self.filename)
                FileTree(self)
        except Exception:
            pass

    def show_file_tree(self, *args):#显示文件树
        self.control_key = False
        self.textarea.isControlPressed = False
        FileTree(self)
        return 'break'

    def save(self,*args):# 保存文件中所做的更改
        #如果用快捷键打开时，ctrl键状态为None，则不执行后续代码
        if args and not self.control_key:
            return
        self.control_key = False
        if self.filename != self.dirname:
            try:
                textarea_content = self.textarea.get("1.0", "end-1c")
                self.total_word = len(textarea_content)
                with open(self.filename, 'w', encoding="utf-8") as f:
                    f.write(textarea_content)
                self.set_window_title(self.filename)
                self.statusbar.update_status('saved')
                if self.filename == self.loader.settings_path:
                    self.reconfigure_settings()
                    self.menubar.reconfigure_settings()
                self.updateScript()
                self.textEdited = False
                if not self.syntax_highlighter.auto_highlight:
                    self.switch_highlight()#启用语法高亮
            except Exception as e:
                pass
        else:
            self.save_as()

    def updateScript(self):# 脚本内容更新，通知执行线程重启
        GV["TEXT"] = self.textarea.get("1.0", "end-1c")
        GV["THREAD_ID"] += 1
        nowTime = time.strftime("%Y年%m月%d日 %H:%M:%S", time.strptime(time.ctime())) # '2023年08月23日  20:18:52'
        print(f"({nowTime})\t\t脚本已加载")
        self.total_word = len(GV["TEXT"])

    def save_as(self, *args):# 将文件保存为特定名称
        #如果大写切换键状态是关，则会调用self.save()
        #如果用快捷键打开时，ctrl键状态为None，则不执行后续代码
        if args and not self.control_key:
            return
        # 释放ctrl键
        self.control_key = False
        try:
            ask_result = filedialog.asksaveasfilename(
                parent=self.master,
                title='另存为',
                initialdir=self.dirname,
                filetypes=[('Lua Scripts', '*.lua'),])
            if ask_result:
                self.filename = ask_result
            else:
                return
            textarea_content = self.textarea.get("1.0", "end-1c")
            self.total_word = len(textarea_content)
            with open(self.filename, 'w', encoding="utf-8") as f:
                f.write(textarea_content)
            self.set_window_title(self.filename)
            self.statusbar.update_status('saved')
            self.updateScript()
            self.save_script_path()#保存脚本路径
            self.textEdited = False
            if not self.syntax_highlighter.auto_highlight:
                self.switch_highlight()#启用语法高亮
        except Exception as e:
            pass

    def quit_save(self):#退出程序时保存文件
        try:
            os.path.isfile(self.filename)
            self.save()
        except Exception:
            self.save_as()
        os.kill(os.getpid(), 9)

    def restore_window(self):#恢复窗口显示
        self.master.deiconify()  # 恢复窗口
        self.master.lift()  # 将窗口置于最前

    def exit_application(self):#退出软件
        os.kill(os.getpid(), 9)

    def minimize_to_tray(self):# 隐藏窗口
        self.master.withdraw()

    def on_closing(self):#关闭软件时检查是否需要保存
        if not self.textEdited:#内容没有变化，无需保存，直接退出程序
            os.kill(os.getpid(), 9)
        message = tk.messagebox.askyesnocancel("关闭时保存", "您想在关闭前保存更改吗？")
        if message == True:
            self.quit_save()
        elif message == False:
            os.kill(os.getpid(), 9)
        else:
            return

    def select_all_text(self, *args):# 选择编辑器中的所有书面文本
        self.textarea.tag_add(tk.SEL, '1.0', tk.END)
        self.textarea.mark_set(tk.INSERT, '1.0')
        self.textarea.see(tk.INSERT)
        return 'break'

    def apply_hex_color(self, key_event):# 为文件内容提供十六进制颜色以便更好地理解
        # 释放ctrl键
        self.control_key = False
        new_color = self.menubar.open_color_picker()
        try:
            sel_start = self.textarea.index(tk.SEL_FIRST)
            sel_end = self.textarea.index(tk.SEL_LAST)
            self.textarea.delete(sel_start, sel_end)
            self.textarea.insert(sel_start, new_color)
        except tk.TclError:
            pass

    def _on_change(self, key_event):
        self.linenumbers.redraw()

    def _on_mousewheel(self, event):
        if self.control_key:
            self.change_font_size(1 if event.delta > 0 else -1)

    def _on_linux_scroll_up(self, _):
        if self.control_key:
            self.change_font_size(1)
            if self.filename == self.loader.settings_path:
                self.syntax_highlighter.initial_highlight()

    def _on_linux_scroll_down(self, _):
        if self.control_key:
            self.change_font_size(-1)
            if self.filename == self.loader.settings_path:
                self.syntax_highlighter.initial_highlight()

    def change_font_add(self):
        self.change_font_size(1)

    def change_font_sub(self):
        self.change_font_size(-1)

    def change_font_size(self, delta):
        self.font_size = self.font_size + delta
        min_font_size = 6
        self.font_size = min_font_size if self.font_size < min_font_size else self.font_size
        font_size_consoleText = self.font_size - 3
        if font_size_consoleText < 3:
            font_size_consoleText = 3

        self.font_style = tk_font.Font(family=self.font_family,
                                       size=self.font_size)

        font_style_consoleText = tk_font.Font(family="宋体",
                                       size=font_size_consoleText)

        self.italics = tk_font.Font(family=self.font_family,
                                    size=self.font_size,
                                    slant='italic')

        self.bold = tk_font.Font(family=self.font_family,
                                 size = self.font_size,
                                 weight='bold')

        self.header1 = tk_font.Font(family=self.font_family,
                                    size = self.font_size + 15,
                                    weight='bold')

        self.header2 = tk_font.Font(family=self.font_family,
                                    size = self.font_size + 7,
                                    weight='bold')

        self.textarea.configure(font=self.font_style)
        self.consoleText.configure(font=font_style_consoleText)
        self.syntax_highlighter.text.tag_configure("Token.Name.Builtin.Pseudo",font=self.italics)
        self.syntax_highlighter.text.tag_configure("Token.Keyword.Type",font=self.italics)
        self.syntax_highlighter.text.tag_configure("Token.Keyword.Declaration",font=self.italics)
        self.syntax_highlighter.text.tag_configure("Token.Generic.Emph",font=self.italics)
        self.syntax_highlighter.text.tag_configure("Token.Generic.Strong",font=self.bold)
        self.syntax_highlighter.text.tag_configure("Token.Generic.Heading",font=self.header1)
        self.syntax_highlighter.text.tag_configure("Token.Generic.Subheading",font=self.header2)
        self.set_new_tab_width()
        
        _settings = self.loader.load_settings_data()
        _settings['font_size'] = self.font_size
        self.loader.store_settings_data(_settings)

        if self.filename == self.loader.settings_path:
            self.clear_and_replace_textarea()

    def _on_keydown(self, event):
        if event.keycode in [17, 37, 109, 262401, 270336, 262145]:
            self.control_key = True
            self.textarea.isControlPressed = True
        else:
            self.statusbar.update_status('hide')

    def key_release(self, event):
        self.control_key = False
        self.textarea.isControlPressed = False
        self.change_title()

    def change_title(self):#改变标题
        word_count = len(self.textarea.get("1.0", "end-1c"))
        if word_count != self.total_word:#总字数有变化，标题加符号*
            self.total_word = word_count
            self.master.title(f'{self.filename} - 红盒*')
            self.textEdited = True
            if self.syntax_highlighter.auto_highlight:
                self.switch_highlight()#关闭语法高亮

    def show_find_window(self, event=None):
        self.textarea.tag_configure('find_match', background=self.text_selection_bg_clr)
        self.textarea.bg_color = self.bg_color
        self.textarea.fg_color = self.menu_fg
        self.textarea.active_fg = self.menubar_fg_active
        self.textarea.active_bg = self.menubar_bg_active
        FindWindow(self.textarea)
        self.control_key = False
        self.textarea.isControlPressed = False

    def select_all(self):
        self.selection_set(0, 'end')

    def autoclose_base(self, symbol):
        index = self.textarea.index(tk.INSERT)
        self.textarea.insert(index, symbol)
        self.textarea.mark_set(tk.INSERT, index)

    def autoclose_parens(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_parentheses and not second_char.isalnum():
            self.autoclose_base(')')

    def autoclose_curly_brackets(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_curlybraces and not second_char.isalnum():
            self.autoclose_base('}')

    def autoclose_square_brackets(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_squarebrackets and not second_char.isalnum():
            self.autoclose_base(']')

    def autoclose_double_quotes(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_doublequotes and not second_char.isalnum():
            self.autoclose_base('"')

    def autoclose_single_quotes(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_singlequotes and not second_char.isalnum():
            self.autoclose_base("'")

    def get_indent_level(self):
        text = self.textarea
        line = text.get('insert linestart', 'insert lineend')
        match = re.match(r'^(\s+)', line)# 匹配字符串开头的空白字符
        if match:
            whitespace = match.group(1)
            tab_count = whitespace.count('\t')
            current_indent = (int((len(match.group(0)) - tab_count) / 4) + tab_count)
        else:
            current_indent = 0
        return current_indent

    def auto_indentation(self):
        text = self.textarea
        new_indent = self.get_indent_level()
        text.insert('insert', '\n' + '\t' * new_indent)

    def auto_block_indentation(self, event):
        prev_char, second_char, _, _ = self.get_chars_in_front_and_back()
        text = self.textarea
        if prev_char == ':':
            current_indent = self.get_indent_level()
            new_indent = current_indent + 1
            text.insert('insert', '\n' + '\t' * new_indent)
            return 'break'
        elif prev_char in '{[(' and second_char in '}])':
            current_indent = self.get_indent_level()
            new_indent = current_indent + 1
            text.insert('insert', '\n\n')
            text.insert('insert', '\t' * current_indent)
            index = text.index(tk.INSERT)
            text.mark_set('insert', str(round(float(index) - 1, 1)))
            text.insert('insert', '\t' * new_indent)
            return 'break'
        else:
            self.auto_indentation()
            return 'break'

    def get_chars_in_front_and_back(self):
        index = self.textarea.index(tk.INSERT)
        first_pos = f'{str(index)}-1c'
        end_second_pos = f'{str(index)}+1c'
        first_char = self.textarea.get(first_pos, index)
        second_char = self.textarea.get(index, end_second_pos)
        return (first_char, second_char, index, end_second_pos)

    def backspace_situations(self, event):
        first_char, second_char, index, end_second_pos = self.get_chars_in_front_and_back()

        if first_char == "'" and second_char == "'":
            self.textarea.delete(index, end_second_pos)
        elif first_char == '"' and second_char == '"':
            self.textarea.delete(index, end_second_pos)
        elif first_char == '(' and second_char == ')':
            self.textarea.delete(index, end_second_pos)
        elif first_char == '{' and second_char == '}':
            self.textarea.delete(index, end_second_pos)
        elif first_char == '[' and second_char == ']':
            self.textarea.delete(index, end_second_pos)

    def tab_text_sub(self, *event):# 减少缩进
        index = self.textarea.index("sel.first linestart")
        last = self.textarea.index("sel.last linestart")
        
        if last != index:#多行
            count = int(float(last) - float(index) + 1)
            for i in range(count):
                float_index = float(index) + i
                start_index = str(float_index)
                str_index = start_index.split(".")[0]
                end_index = str(float_index + 1.0)
                if self.textarea.get(start_index, end_index)[:1] == "\t":
                    self.textarea.delete(start_index)
                elif self.textarea.get(start_index, end_index)[:4] == "    ":
                        self.textarea.delete(start_index, str_index + ".4")
        else:#单行
            index = self.textarea.index("insert linestart")
            str_index = index.split(".")[0]
            if self.textarea.get(index, 'end')[:1] == "\t":
                self.textarea.delete(index)
            elif self.textarea.get(index, 'end')[:4] == "    ":
                self.textarea.delete(index, str_index + ".4")
        return "break"

    def tab_text_add(self, *event):# 增加缩进
        index = self.textarea.index("sel.first linestart")
        last = self.textarea.index("sel.last linestart")

        if last != index:#多行
            count = int(float(last) - float(index) + 1)
            for i in range(count):
                str_index = str(float(index) + i)
                self.textarea.insert(str_index, '\t')
        else:#单行
            index = self.textarea.index("insert linestart")
            self.textarea.insert(index, '\t')
        return "break"

    def code_uncomment(self, *args):# 取消代码注释
        index = self.textarea.index("sel.first linestart")
        last = self.textarea.index("sel.last linestart")

        if last != index:# 多行
            count = int(float(last) - float(index) + 1)
            for i in range(count):
                float_index = float(index) + i
                sta_index = str(float_index)
                str_index = sta_index.split(".")[0]
                end_index = str(float_index + 1.0)
                text = self.textarea.get(sta_index, end_index).split("\n")[0]
                index_find = text.find("--")
                if index_find == -1:#没找到符号#，则跳过一次循环
                    continue
                if index_find != 0:#符号--不是第1个
                    #判断#前面是不是全都是 " " 或 "\t"
                    contains_non_blank = 0
                    for j in text[:index_find]:
                        if j not in (" ", "\t", "\n"):
                            contains_non_blank = 1
                            break
                    if contains_non_blank == 1:#包含非空字符，则跳过一次循环
                        continue
                    add_index_1 = "." + str(index_find)
                    add_index_2 = "." + str(index_find + 3)
                    add_index_3 = "." + str(index_find + 2)
                    start_index = str_index + add_index_1
                    end_index_1 = str_index + add_index_2
                    end_index_2 = str_index + add_index_3
                    if text[index_find:index_find+3] == "-- ":
                        self.textarea.delete(start_index, end_index_1)
                    elif text[index_find:index_find+2] == "--":
                        self.textarea.delete(start_index, end_index_2)
                else:
                    if text[index_find:index_find+3] == "-- ":
                        self.textarea.delete(sta_index, str_index + ".3")
                    elif text[index_find:index_find+2] == "--":
                        self.textarea.delete(sta_index, str_index + ".2")
        else:# 单行
            index = self.textarea.index("insert linestart")
            str_index = index.split(".")[0]
            text = self.textarea.get(index, 'end').split("\n")[0]
            index_find = text.find("--")
            if index_find == -1:#没找到符号--，则返回
                return
            if index_find != 0:#符号--不是第1个
                #判断--前面是不是全都是 " " 或 "\t"
                contains_non_blank = 0
                for i in text[:index_find]:
                    if i not in (" ", "\t", "\n"):
                        contains_non_blank = 1
                        break
                if contains_non_blank == 1:#包含非空字符，则返回
                    return
                add_index_1 = "." + str(index_find)
                add_index_2 = "." + str(index_find + 3)
                add_index_3 = "." + str(index_find + 2)
                start_index = str_index + add_index_1
                end_index_1 = str_index + add_index_2
                end_index_2 = str_index + add_index_3
                if text[index_find:index_find+3] == "-- ":
                    self.textarea.delete(start_index, end_index_1)
                elif text[index_find:index_find+2] == "--":
                    self.textarea.delete(start_index, end_index_2)
            else:
                if text[index_find:index_find+3] == "-- ":
                    self.textarea.delete(index, str_index + ".3")
                elif text[index_find:index_find+2] == "--":
                    self.textarea.delete(index, str_index + ".2")
        self.syntax_highlighter.initial_highlight()
        self.change_title()
        return "break"

    def code_comment(self, *args):# 代码注释
        index = self.textarea.index("sel.first linestart")
        last = self.textarea.index("sel.last linestart")

        if last != index:# 多行
            count = int(float(last) - float(index) + 1)
            for i in range(count):
                float_index = float(index) + i
                start_index = str(float_index)
                str_index = start_index.split(".")[0]
                end_index = str(float_index + 1.0)
                text = self.textarea.get(start_index, end_index).split("\n")[0]
                if len(text) == 0:#空行不需要注释
                    continue
                index_find = text.find("--")
                if index_find != -1:#找到符号--，则判断前面是否都是空白字符，如果是，则说明已经注释了
                    if index_find == 0:#符号--在第1个
                        continue
                    # 判断#前面是不是全都是 " " 或 "\t"
                    index_non_blank = 0
                    index_now = 0
                    text_new = text.split("--")[0]
                    for j in text_new:
                        index_now += 1
                        if j not in (" ", "\t", "\n"):
                            index_non_blank = index_now
                            break
                    if index_non_blank != 0:#符号--的前面有非空字符
                        if index_non_blank == 1:
                            self.textarea.insert(start_index, "-- ")
                        else:
                            add_index = "." + str(index_non_blank - 1)
                            self.textarea.insert(str_index + add_index, "-- ")
                    else:#符号--的前面是空字符，说明已经注释了
                        continue
                else:#没找到符号--
                    # 找第一个非空字符的位置
                    index_non_blank = 0
                    index_now = 0
                    for j in text:
                        index_now += 1
                        if j not in (" ", "\t", "\n"):
                            index_non_blank = index_now
                            break
                    if index_non_blank == 0:#全是空字符，则不需要注释
                        continue
                    if index_non_blank == 1:
                        self.textarea.insert(start_index, "-- ")
                    else:
                        add_index = "." + str(index_non_blank - 1)
                        self.textarea.insert(str_index + add_index, "-- ")
        else:# 单行
            index = self.textarea.index("insert linestart")
            str_index = index.split(".")[0]
            text = self.textarea.get(index, 'end').split("\n")[0]
            if len(text) == 0:#空行不需要注释
                return
            index_find = text.find("--")
            if index_find != -1:#找到符号--，则判断前面是否都是空白字符，如果是，则说明已经注释了
                if index_find == 0:#符号--在第1个
                    return
                # 判断#前面是不是全都是 " " 或 "\t"
                index_non_blank = 0
                index_now = 0
                text_new = text.split("--")[0]
                for i in text_new:
                    index_now += 1
                    if i not in (" ", "\t", "\n"):
                        index_non_blank = index_now
                        break
                if index_non_blank != 0:#符号--的前面有非空字符
                    if index_non_blank == 1:
                        self.textarea.insert(index, "-- ")
                    else:
                        add_index = "." + str(index_non_blank - 1)
                        self.textarea.insert(str_index + add_index, "-- ")
                else:#符号--的前面是空字符，说明已经注释了
                    return
            else:#没找到符号--
                index_non_blank = 0
                index_now = 0
                for i in text:
                    index_now += 1
                    if i not in (" ", "\t", "\n"):
                        index_non_blank = index_now
                        break
                if index_non_blank == 0:#全是空字符，则不需要注释
                    return
                if index_non_blank == 1:
                    self.textarea.insert(index, "-- ")
                else:
                    add_index = "." + str(index_non_blank - 1)
                    self.textarea.insert(str_index + add_index, "-- ")
        self.syntax_highlighter.initial_highlight()
        self.change_title()
        return "break"

    def highlight_after_delay(self, event):
        def waiting_to_execute():
            time.sleep(0.5)
            self.syntax_highlighter.initial_highlight()
        t1 = threading.Thread(target=waiting_to_execute)
        t1.start()

    def bind_shortcuts(self, *args):
        text = self.textarea
        text.bind('<Control-n>', self.new_file)
        text.bind('<Control-o>', self.open_file)
        text.bind('<Control-s>', self.save)
        text.bind('<Control-S>', self.save_as)
        text.bind('<Control-KeyRelease-e>', self.code_comment)
        text.bind('<Control-KeyRelease-q>', self.code_uncomment)
        text.bind('<Control-KeyRelease-b>', self.context_menu.bold)
        text.bind('<Control-KeyRelease-h>', self.context_menu.hightlight)
        text.bind('<Control-KeyRelease-a>', self.select_all_text)
        text.bind('<Control-KeyRelease-m>', self.apply_hex_color)
        text.bind('<Control-KeyRelease-f>', self.show_find_window)
        text.bind('<Control-KeyRelease-p>', self.load_previous_file)
        text.bind('<Control-KeyRelease-t>', self.show_file_tree)
        text.bind('<Control-KeyRelease-v>', self.syntax_highlighter.initial_highlight)
        text.bind('<Control-KeyRelease-z>', self.syntax_highlighter.initial_highlight)
        text.bind('<Control-KeyRelease-y>', self.syntax_highlighter.initial_highlight)
        text.bind('<<Change>>', self._on_change)
        text.bind('<Configure>', self._on_change)
        text.bind('<Button-3>', self.context_menu.popup)
        text.bind('<MouseWheel>', self._on_mousewheel)
        text.bind('<Button-4>', self._on_linux_scroll_up)
        text.bind('<Button-5>', self._on_linux_scroll_down)
        text.bind('<Key>', self._on_keydown)
        text.bind('<KeyRelease>', self.key_release)
        text.bind('<Shift-asciitilde>', self.syntax_highlighter.initial_highlight)
        text.bind('<Shift-parenleft>', self.autoclose_parens)
        text.bind('<bracketleft>', self.autoclose_square_brackets)
        text.bind('<quoteright>', self.autoclose_single_quotes)
        text.bind('<quotedbl>', self.autoclose_double_quotes)
        text.bind('<braceleft>', self.autoclose_curly_brackets)
        text.bind('<Return>', self.auto_block_indentation)
        text.bind('<BackSpace>', self.backspace_situations)
        text.bind('<Control-KeyRelease-L>', self.toggle_linenumbers)
        text.bind('<Control-KeyRelease-H>', self.switch_highlight)
        text.bind('<KeyPress-Tab>', self.tab_text_add)
        text.bind('<Shift-Tab>', self.tab_text_sub)


class Implemented:#已实现的功能接口
    def __init__(self):
        self.SendInput = SendInputApi()

    def GetExecThreadId(self):#获取执行线程ID
        return GV["THREAD_ID"]

    def isEnableGate(self):# lua脚本运行闸门
        enableGate = False
        if GV["EVENT"] != GV["LAST_EVENT"]:
            GV["LAST_EVENT"] = GV["EVENT"]
            enableGate = True
        if GV["EVENT"] == "M_PRESSED":
            enableGate = True
        if GV["ARG"] != GV["LAST_ARG"]:
            GV["LAST_ARG"] = GV["ARG"]
            enableGate = True
        if GV["FAMILY"] != GV["LAST_FAMILY"]:
            GV["LAST_FAMILY"] = GV["FAMILY"]
            enableGate = True
        return enableGate

    def OnEventEvent(self):# 返回OnEvent所需参数event
        return GV["EVENT"]

    def OnEventActivated(self):# 配置文件已被激活
        GV["EVENT"] = "PROFILE_ACTIVATED"

    def OnEventDeactivated(self):# 配置文件已被反激活
        if GV["EVENT"] == "PROFILE_ACTIVATED":
            GV["EVENT"] = "PROFILE_DEACTIVATED"

    def OnEventArg(self):# 返回OnEvent所需参数arg
        return GV["ARG"]

    def OnEventFamily(self):# 返回OnEvent所需参数family
        return GV["FAMILY"]

    def GetMKeyState(self, family=""):# 返回当前 M Key 状态值
        print("GetMKeyState 未实现")

    def SetMKeyState(self, mkey="", family=""):# 可以设置当前 M keys 激活状态
        if GV["LAST_EVENT"] != "M_PRESSED":
            GV["EVENT"] = "M_PRESSED"

    def Sleep(self, timeout):# 休眠
        time.sleep(round((timeout / 1000), 3))

    def OutputLogMessage(self, Message):# 将输出日志消息至脚本编辑器的控制台操作窗中
        print(Message, end="")

    def GetRunningTime(self):# 将返回以毫秒为单位的执行脚本总时间
        return int((time.time() - GV["START_TIME"]) * 1000)

    def GetDate(self, *args):# 方法将获取已格式化的当前时间
        return time.strftime("%m/%d/%y %H:%M:%S", time.strptime(time.ctime()))

    def ClearLog(self):# 清空脚本编辑器控制台中的输出内容
        print("__ClearLog__")

    def PressKey(self, keyname):# 方法可被用于模拟键盘按键按下动作
        self.SendInput.keyDown(keyname)

    def ReleaseKey(self, keyname):# 方法可被用于模拟键盘按键释放动作
        self.SendInput.keyUp(keyname)

    def PressAndReleaseKey(self, keyname):# 方法可被用于模拟键盘按键按下动作并跟随按键释放动作
        self.SendInput.press(keyname)

    def IsModifierPressed(self, keyname):# 方法可用于确定某修饰键是否被按下
        if keyname == "lalt":
            if GV["KEYBOARD_LEFT_ALT"] == 1:
                return True
            return False
        elif keyname == "ralt":
            if GV["KEYBOARD_RIGHT_ALT"] == 1:
                return True
            return False
        elif keyname == "alt":
            if GV["KEYBOARD_LEFT_ALT"] == 1 == GV["KEYBOARD_RIGHT_ALT"]:
                return True
            return False
        elif keyname == "lshift":
            if GV["KEYBOARD_LEFT_SHIFT"] == 1:
                return True
            return False
        elif keyname == "rshift":
            if GV["KEYBOARD_RIGHT_SHIFT"] == 1:
                return True
            return False
        elif keyname == "shift":
            if GV["KEYBOARD_LEFT_SHIFT"] == 1 == GV["KEYBOARD_RIGHT_SHIFT"]:
                return True
            return False
        elif keyname == "lctrl":
            if GV["KEYBOARD_LEFT_CTRL"] == 1:
                return True
            return False
        elif keyname == "rctrl":
            if GV["KEYBOARD_RIGHT_CTRL"] == 1:
                return True
            return False
        elif keyname == "ctrl":
            if GV["KEYBOARD_LEFT_CTRL"] == 1 == GV["KEYBOARD_RIGHT_CTRL"]:
                return True
            return False
        return False

    def PressMouseButton(self, button):# 模拟鼠标左键、中键或右键被按下
        self.SendInput.mouseDown(button=button)

    def ReleaseMouseButton(self, button):# 模拟鼠标左键、中键或右键被释放
        self.SendInput.mouseUp(button=button)

    def PressAndReleaseMouseButton(self, button):# 模拟鼠标左键、中键或右键按下并释放
        self.SendInput.click(button=button)

    def IsMouseButtonPressed(self, button):# 可用于确定某鼠标按键是否被按下
        # 1	鼠标左键
        # 2	鼠标中键
        # 3	鼠标右键
        # 4	鼠标侧键
        # 4	鼠标按键 X1
        # 5	鼠标按键 X2
        if button == 1:
            if GV["MOUSE_LEFT"] == 1:
                return True
            return False
        elif button == 2:
            if GV["MOUSE_MIDDLE"] == 1:
                return True
            return False
        elif button == 3:
            if GV["MOUSE_RIGHT"] == 1:
                return True
            return False
        elif button == 4:
            if GV["MOUSE_SIDE_X1"] == 1:
                return True
            return False
        elif button == 5:
            if GV["MOUSE_SIDE_X2"] == 1:
                return True
            return False
        return False

    def LastKeyClick(self):# 获取最后一次单击的键盘按键名
        return GV["LAST_KEY_CLICK"]

    def MoveMouseTo(self, x, y):# 移动鼠标指针至屏幕中的目标绝对坐标位置
        # -- 移动鼠标至左上角
        # MoveMouseTo(0, 0)
        # -- 移动鼠标至屏幕中央
        # MoveMouseTo(32767, 32767)
        # -- 移动鼠标至右下角
        # MoveMouseTo(65535, 65535)
        MOUSE_LEFT = GV["MOUSE_LEFT"]
        self.SendInput.moveTo(x, y)
        if GV["MOUSE_LEFT"] != MOUSE_LEFT:# 防止鼠标移动后，左键按下或释放状态错乱
            GV["MOUSE_LEFT"] = MOUSE_LEFT

    def MoveMouseWheel(self, click):# 可被用于模拟鼠标滚轮滚动
        print("MoveMouseWheel 未实现")

    def MoveMouseRelative(self, x, y):# 可被用于模拟鼠标相对当前坐标的偏移量
        MOUSE_LEFT = GV["MOUSE_LEFT"]
        if x:
            x = int(x)
        else:
            x = 0
        if y:
            y = int(y)
        else:
            y = 0
        self.SendInput.moveRel(x, y)
        if GV["MOUSE_LEFT"] != MOUSE_LEFT:#防止鼠标移动后，左键按下或释放状态错乱
            GV["MOUSE_LEFT"] = MOUSE_LEFT

    def MoveMouseToVirtual(self, x, y):# 可被用于在多个屏幕中移动鼠标指针至当前屏幕中的目标绝对坐标位置
        # -- 移动鼠标至虚拟桌面中的左上角
        # MoveMouseToVirtual(0, 0)
        # -- 移动鼠标至虚拟桌面中的中央
        # MoveMouseToVirtual (32767, 32767)
        # -- 移动鼠标至虚拟桌面中的右下角
        # MoveMouseToVirtual (65535, 65535)
        print("MoveMouseToVirtual 未实现")

    def GetMousePosition(self):# 可被用于获取鼠标指针当前相对标准坐标
        return self.SendInput.position()

    def OutputLCDMessage(self, text="", timeout=0):# 可被用于向LCD 添加单行文本
        # -- 使用默认超时显示文本
        # OutputLCDMessage("Hello world")
        # -- 显示文本并设置 2 秒超时时间
        # OutputLCDMessage("Hello world", 2000)
        print("OutputLCDMessage 未实现")

    def ClearLCD(self):# 可用于清除由脚本输出在 LED 中的字符串
        # -- 清理 LED 已显示内容并输出两条文本信息
        # ClearLCD () OutputLCDMessage("Hello world1") OutputLCDMessage("Hello world2")
        print("ClearLCD 未实现")

    def PlayMacro(self, macroname=""):# 可被用于播放已存在宏脚本
        # -- 播放已存在宏脚本
        # PlayMacro("my macro");
        print("PlayMacro 未实现")

    def AbortMacro(self):# 可被用于中断当前任何已在播放的宏脚本
        # -- 播放宏脚本
        # PlayMacro("my macro")
        # -- 等待100 毫秒并将正在播放的宏脚本中断
        # AbortMacro()
        print("AbortMacro 未实现")

    def IsKeyLockOn(self, key):# 可用于确定锁定键是否处于启用状态
        if key == "capslock":#大小写锁定
            if ctypes.windll.user32.GetKeyState(0x14):
                return True
        elif key == "numlock":#数字键锁定
            if ctypes.windll.user32.GetKeyState(0x90):
                return True
        elif key == "scrolllock":#滚动锁定
            if ctypes.windll.user32.GetKeyState(0x91):
                return True
        return False

    def SetBacklightColor(self, red=0, green=0, blue=0, family=""):# 被用于设置自定义设备背光灯颜色
        # -- 设置背光灯为红色
        # SetBacklightColor(255, 0, 0);
        print("SetBacklightColor 未实现")

    def OutputDebugMessage(self, Message):# 将发送日志消息至 Windows 脚本调试器
        # -- 输出文本 "Hello World"
        # OutputDebugMessage("Hello World %d\n", 2007)
        print("OutputDebugMessage 未实现")

    def SetMouseDPITable(self, value=[], index=0):# 可向已支持的游戏鼠标设置当前 DPI 表中的数值
        # -- 设置 DPI 数值为 {500, 1000, 1500, 2000, 2500}
        # -- 默认状态下，500 DPI 将被设为当前 DPI 数值
        # SetMouseDPITable({500, 1000, 1500, 2000, 2500})
        # -- 设置 DPI 数值为 {500, 2500} 并设置第二个数值为当前 DPI 数值
        # SetMouseDPITable({500, 2500}, 2)
        print("SetMouseDPITable 未实现")

    def SetMouseDPITableIndex(self, index):# 可向已支持的游戏鼠标通过DPI 表索引值设置 DPI
        # -- 设置初始 DPI数值为 {500, 1000, 1500, 2000, 2500}
        # -- 设置当前 DPI 为表中第三项 (1500 DPI)
        # SetMouseDPITableIndex(3);
        print("SetMouseDPITableIndex 未实现")

    def EnablePrimaryMouseButtonEvents(self, enable):# 启用鼠标按键 1 事件报告
        # -- 启用鼠标按键 1 事件报告
        # EnablePrimaryMouseButtonEvents(true);
        # -- 禁用鼠标按键 1 事件报告
        # EnablePrimaryMouseButtonEvents(false);
        if enable:
            GV['ENABLE_MOUSE_LEFT'] = True
        else:
            GV['ENABLE_MOUSE_LEFT'] = False

    def typewrite(self, message):#连续单击键盘按键
        self.SendInput.typewrite(message)

    def GetMouseAcceleration(self):#查询鼠标加速度是否启用
        # 勾选为1 不勾选为0
        p_epp = ctypes.c_void_p()
        ctypes.windll.user32.SystemParametersInfoA(0x0003, 0, ctypes.pointer(p_epp), 0)
        if p_epp.value:
            return True
        return False

    def SetMouseAcceleration(self, action):#设置启用或关闭鼠标加速度
        if action: # 勾选  启用
            EPP_ON = [1,1,1]
            ctypes.windll.user32.SystemParametersInfoA(0x0004, 0, (ctypes.c_int * 3)(*EPP_ON), 0)
        else: # 取消勾选  关闭
            EPP_OFF = [0,0,0]
            ctypes.windll.user32.SystemParametersInfoA(0x0004, 0, (ctypes.c_int * 3)(*EPP_OFF), 0)

    def GetMouseSpeed(self):#查询鼠标灵敏度
        p_mouse_speed = ctypes.c_void_p()
        ctypes.windll.user32.SystemParametersInfoA(0x0070, 0, ctypes.pointer(p_mouse_speed), 0)
        mouseSpeed = int(p_mouse_speed.value)
        if mouseSpeed:
            return mouseSpeed
        else:
            return 10

    def SetMouseSpeed(self, speed):#设置鼠标灵敏度
        # 设置鼠标灵敏度为10档 范围在1 - 20之间
        if speed < 1:
            speed = 1
        elif speed > 20:
            speed = 20
        ctypes.windll.user32.SystemParametersInfoA(0x0071, 0, speed, 0)

    def IsActiveWindows(self, exeName):# 判断当前活动窗口是否指定进程 参数："xxx.exe"
        _user32 = ctypes.windll.user32
        pid = ctypes.c_ulong()
        _user32.GetWindowThreadProcessId(_user32.GetForegroundWindow(), ctypes.pointer(pid))
        process_list = psutil.Process(pid.value)# pid.value = 当前活动窗口的pid
        process_name = process_list.name()# process_name = 当前活动窗口的进程名
        if exeName in process_name:# exeName = TslGame.exe
            return True
        return False


class SCRIPT_EXECUTION(threading.Thread):#脚本执行线程
    def run(self):
        CurrentThreadId = GV["THREAD_ID"]
        impInterface = Implemented()#已实现的功能接口
        lua = LuaRuntime(unpack_returned_tuples=True)
        # 将 Python 函数注册到 Lua 中 lua5.1
        # for i in lua.globals():
        #     print(i)
        # string
        # xpcall
        # package
        # tostring
        # print
        # os
        # unpack
        # require
        # getfenv
        # setmetatable
        # next
        # assert
        # tonumber
        # io
        # rawequal
        # collectgarbage
        # getmetatable
        # module
        # rawset
        # python
        # math
        # debug
        # pcall
        # table
        # newproxy
        # type
        # coroutine
        # _G
        # select
        # gcinfo
        # pairs
        # rawget
        # loadstring
        # ipairs
        # _VERSION
        # dofile
        # setfenv
        # load
        # error
        # loadfile
        lua.globals().python = None
        lua.globals().CurrentThreadId = CurrentThreadId
        lua.globals().GetExecThreadId = impInterface.GetExecThreadId
        lua.globals().isEnableGate = impInterface.isEnableGate
        lua.globals().OnEventEvent = impInterface.OnEventEvent
        lua.globals().OnEventArg = impInterface.OnEventArg
        lua.globals().OnEventFamily = impInterface.OnEventFamily
        lua.globals().GetMKeyState = impInterface.GetMKeyState
        lua.globals().SetMKeyState = impInterface.SetMKeyState
        lua.globals().Sleep = impInterface.Sleep
        lua.globals().OutputLogMessage = impInterface.OutputLogMessage
        lua.globals().GetRunningTime = impInterface.GetRunningTime
        lua.globals().GetDate = impInterface.GetDate
        lua.globals().ClearLog = impInterface.ClearLog
        lua.globals().PressKey = impInterface.PressKey
        lua.globals().ReleaseKey = impInterface.ReleaseKey
        lua.globals().PressAndReleaseKey = impInterface.PressAndReleaseKey
        lua.globals().IsModifierPressed = impInterface.IsModifierPressed
        lua.globals().PressMouseButton = impInterface.PressMouseButton
        lua.globals().ReleaseMouseButton = impInterface.ReleaseMouseButton
        lua.globals().PressAndReleaseMouseButton = impInterface.PressAndReleaseMouseButton
        lua.globals().IsMouseButtonPressed = impInterface.IsMouseButtonPressed
        lua.globals().MoveMouseTo = impInterface.MoveMouseTo
        lua.globals().MoveMouseWheel = impInterface.MoveMouseWheel
        lua.globals().MoveMouseRelative = impInterface.MoveMouseRelative
        lua.globals().MoveMouseToVirtual = impInterface.MoveMouseToVirtual
        lua.globals().GetMousePosition = impInterface.GetMousePosition
        lua.globals().OutputLCDMessage = impInterface.OutputLCDMessage
        lua.globals().ClearLCD = impInterface.ClearLCD
        lua.globals().PlayMacro = impInterface.PlayMacro
        lua.globals().AbortMacro = impInterface.AbortMacro
        lua.globals().IsKeyLockOn = impInterface.IsKeyLockOn
        lua.globals().SetBacklightColor = impInterface.SetBacklightColor
        lua.globals().OutputDebugMessage = impInterface.OutputDebugMessage
        lua.globals().SetMouseDPITable = impInterface.SetMouseDPITable
        lua.globals().SetMouseDPITableIndex = impInterface.SetMouseDPITableIndex
        lua.globals().EnablePrimaryMouseButtonEvents = impInterface.EnablePrimaryMouseButtonEvents
        # lua.globals().typewrite = impInterface.typewrite
        lua.globals().GetMouseAcceleration = impInterface.GetMouseAcceleration
        lua.globals().SetMouseAcceleration = impInterface.SetMouseAcceleration
        lua.globals().GetMouseSpeed = impInterface.GetMouseSpeed
        lua.globals().SetMouseSpeed = impInterface.SetMouseSpeed
        lua.globals().IsActiveWindows = impInterface.IsActiveWindows
        # lua.globals().OnEventActivated = impInterface.OnEventActivated
        # lua.globals().OnEventDeactivated = impInterface.OnEventDeactivated

        try:
            GV["START_TIME"] = time.time()
            lua.execute(GV["TEXT"] + f'\n while (CurrentThreadId == GetExecThreadId()) do if isEnableGate() then OnEvent(OnEventEvent(), OnEventArg(), OnEventFamily()) end Sleep(1) end')
        except Exception as e:
            print("[ERROR]:", str(e).replace('[string "<python>"]:', 'line '))


class THREAD_VALVE(threading.Thread):#脚本线程阀门
    def run(self):#启动、暂停及重启线程
        while GV["THREAD_ID"] == 0:
            time.sleep(0.1)
        SCRIPT_EXECUTION().start()
        ExecThreadId = GV["THREAD_ID"]
        while True:
            time.sleep(0.1)
            if not GV["THREAD_PAUSE"]:#线程暂停命令
                if ExecThreadId != GV["THREAD_ID"]:
                    ExecThreadId = GV["THREAD_ID"]
                    SCRIPT_EXECUTION().start()#重启线程


def HOOK_MOUSE():#鼠标监听线程
    def on_click(x, y, button, pressed):
        button = str(button)
        if pressed:# 鼠标按键按下
            if "left" in button:# 左键按下
                if GV['ENABLE_MOUSE_LEFT']:
                    GV['MOUSE_LEFT'] = 1
                    GV['EVENT'] = "MOUSE_BUTTON_PRESSED"
                    GV['ARG'] = 1
                    GV['FAMILY'] = "mouse"
            elif "right" in button:# 右键按下
                GV['MOUSE_RIGHT'] = 1
                GV['EVENT'] = "MOUSE_BUTTON_PRESSED"
                GV['ARG'] = 2
                GV['FAMILY'] = "mouse"
            elif "middle" in button:# 中键按下
                GV['MOUSE_MIDDLE'] = 1
                GV['EVENT'] = "MOUSE_BUTTON_PRESSED"
                GV['ARG'] = 3
                GV['FAMILY'] = "mouse"
            elif "x1" in button:# 后侧键x1按下
                GV['MOUSE_SIDE_X1'] = 1
                GV['EVENT'] = "MOUSE_BUTTON_PRESSED"
                GV['ARG'] = 4
                GV['FAMILY'] = "mouse"
            elif "x2" in button:# 前侧键x2按下
                GV['MOUSE_SIDE_X2'] = 1
                GV['EVENT'] = "MOUSE_BUTTON_PRESSED"
                GV['ARG'] = 5
                GV['FAMILY'] = "mouse"
        else:# 鼠标按键弹起
            if "left" in button:# 左键弹起
                if GV['ENABLE_MOUSE_LEFT']:
                    GV['MOUSE_LEFT'] = 0
                    GV['EVENT'] = "MOUSE_BUTTON_RELEASED"
                    GV['ARG'] = 1
                    GV['FAMILY'] = "mouse"
            elif "right" in button:# 右键弹起
                GV['MOUSE_RIGHT'] = 0
                GV['EVENT'] = "MOUSE_BUTTON_RELEASED"
                GV['ARG'] = 2
                GV['FAMILY'] = "mouse"
            elif "middle" in button:# 中键弹起
                GV['MOUSE_MIDDLE'] = 0
                GV['EVENT'] = "MOUSE_BUTTON_RELEASED"
                GV['ARG'] = 3
                GV['FAMILY'] = "mouse"
            elif "x1" in button:# 后侧键x1弹起
                GV['MOUSE_SIDE_X1'] = 0
                GV['EVENT'] = "MOUSE_BUTTON_RELEASED"
                GV['ARG'] = 4
                GV['FAMILY'] = "mouse"
            elif "x2" in button:# 前侧键x2弹起
                GV['MOUSE_SIDE_X2'] = 0
                GV['EVENT'] = "MOUSE_BUTTON_RELEASED"
                GV['ARG'] = 5
                GV['FAMILY'] = "mouse"


    mouse.Listener(on_click=on_click).start()


def HOOK_KEYBOARD():#键盘监听线程
    def on_press(key):# 键盘按键按下
        key = str(key)
        if "pause" in key:# 按下 PAUSE键
            GV['KEYBOARD_PAUSE'] = 1
            if not GV["THREAD_PAUSE"]:
                GV["THREAD_PAUSE"] = True# 跳过重启线程命令
                GV["THREAD_ID"] += 1# lua脚本执行线程会停止
                print("------------------\t暂停脚本运行\t------------------")
            else:
                GV["THREAD_PAUSE"] = False
                print("------------------\t继续脚本运行\t------------------")
        elif "shift_r" in key:# 按下 右 Shift键
            GV['KEYBOARD_RIGHT_SHIFT'] = 1
        elif "shift" in key:# 按下 左 Shift键
            GV['KEYBOARD_LEFT_SHIFT'] = 1
        elif "ctrl_r" in key:# 按下 右 Ctrl键
            GV['KEYBOARD_RIGHT_CTRL'] = 1
        elif "ctrl_l" in key:# 按下 左 Ctrl键
            GV['KEYBOARD_LEFT_CTRL'] = 1
        elif "alt_gr" in key:# 按下 右 Alt键
            GV['KEYBOARD_RIGHT_ALT'] = 1
        elif "alt_r" in key:# 按下 右 Alt键
            GV['KEYBOARD_RIGHT_ALT'] = 1
        elif "alt_l" in key:# 按下 左 Alt键
            GV['KEYBOARD_LEFT_ALT'] = 1


    def on_release(key):# 键盘按键弹起
        key = str(key)
        if "pause" in key:# 弹起 PAUSE键
            GV['KEYBOARD_PAUSE'] = 0
        elif "shift_r" in key:# 弹起 右 Shift键
            GV['KEYBOARD_RIGHT_SHIFT'] = 0
        elif "shift" in key:# 弹起 左 Shift键
            GV['KEYBOARD_LEFT_SHIFT'] = 0
        elif "ctrl_r" in key:# 弹起 右 Ctrl键
            GV['KEYBOARD_RIGHT_CTRL'] = 0
        elif "ctrl_l" in key:# 弹起 左 Ctrl键
            GV['KEYBOARD_LEFT_CTRL'] = 0
        elif "alt_gr" in key:# 弹起 右 Alt键
            GV['KEYBOARD_RIGHT_ALT'] = 0
        elif "alt_r" in key:# 弹起 右 Alt键
            GV['KEYBOARD_RIGHT_ALT'] = 0
        elif "alt_l" in key:# 弹起 左 Alt键
            GV['KEYBOARD_LEFT_ALT'] = 0


    keyboard.Listener(on_press=on_press, on_release=on_release).start()


HOOK_MOUSE()#鼠标监听线程
HOOK_KEYBOARD()#键盘监听线程
THREAD_VALVE().start()#脚本线程阀门

master = tk.Tk()
RedBox(master)#红盒UI主循环线程
