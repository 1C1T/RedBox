# -*- coding: utf-8 -*-
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
from yaml import load, dump, FullLoader
from pygments.lexers import LuaLexer
from pygments import lex
from ctypes import wintypes
from PIL import Image
from lua51 import LuaRuntime
import theRedBox