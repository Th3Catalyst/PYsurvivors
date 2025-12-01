
import json
from enum import Enum

try:
    import config
except Exception:
    pass

try:
    with open(config.file, 'r') as f:
        data = json.load(f)
        buttonStyle = data["button"]


        class ButtonStyles(Enum):

            try:
                margin = buttonStyle['margin']
            except Exception as e:
                print(e)
                margin = 10
            try:
                padding = buttonStyle['padding']
            except Exception:
                padding = 0
            try:
                color = buttonStyle['color']
            except Exception:
                color = "black"
            try:
                bordercolor = buttonStyle['bordercolor']
            except Exception:
                bordercolor = "black"
            try:
                bgcolor = buttonStyle['bgcolor']
            except Exception:
                bgcolor = "grey"
            try:
                bgcolorHover = buttonStyle['bgcolorhover']
            except Exception:
                bgcolorHover = "light grey"
            try:
                anchor = buttonStyle['anchor']
            except Exception:
                anchor = "nw"
            try:
                borderWidth = buttonStyle['borderwidth']
            except Exception:
                borderWidth = 5
except Exception:
    class ButtonStyles(Enum):
        margin = 10
        padding = 0
        bordercolor = "black"
        bgcolor = "grey"
        bgcolorHover = "light grey"
        anchor = "nw"
        color = "black"
        borderWidth = 5
try:
    with open(config.file, 'r') as f:
        data = json.load(f)
        menuStyle = data["menu"]


        class MenuStyles(Enum):
            try:
                margin = menuStyle['margin']
            except Exception:
                margin = 10
            try:
                padding = menuStyle['padding']
            except Exception:
                padding = 0
            try:
                bgcolor = menuStyle['bgcolor']
            except Exception:
                bgcolor = "grey"
            try:
                titlecolor = menuStyle['titlecolor']
            except Exception:
                titlecolor = "white"
            try:
                hrcolor = menuStyle['hrcolor']
            except Exception:
                hrcolor = "black"
            try:
                anchor = menuStyle['anchor']
            except Exception:
                anchor = "nw"
except Exception:
    class MenuStyles(Enum):
        margin = 10
        padding = 0
        bgcolor = "grey"
        anchor = "nw"
        titlecolor = "white"
        hrcolor = "black"
try:
    with open(config.file, 'r') as f:
        data = json.load(f)
        textStyle = data["text"]


        class TextStyles(Enum):
            try:
                margin = textStyle['margin']
            except Exception:
                margin = 10
            try:
                padding = textStyle['padding']
            except Exception:
                padding = 0
            try:
                anchor = textStyle['anchor']
            except Exception:
                anchor = "nw"
            try:
                color = textStyle['color']
            except Exception:
                color = "black"
except Exception:
    class TextStyles(Enum):
        margin = 10
        padding = 0
        anchor = "nw"
        color = "black"
try:
    with open(config.file, 'r') as f:
        data = json.load(f)
        DropdownStyle = data["dropdown"]


        class DropdownStyles(Enum):
            try:
                margin = DropdownStyle['margin']
            except Exception:
                margin = 10
            try:
                padding = DropdownStyle['padding']
            except Exception:
                padding = 0
            try:
                anchor = DropdownStyle['anchor']
            except Exception:
                anchor = "nw"
            try:
                color = DropdownStyle['color']
            except Exception:
                color = "black"
            try:
                bgcolor = DropdownStyle['bgcolor']
            except Exception:
                bgcolor = "white"
            try:
                scaleFactor = DropdownStyle['scaleFactor']
            except Exception:
                scaleFactor = 1
except Exception:
    class DropdownStyles(Enum):
        margin = 10
        padding = 0
        anchor = "nw"
        color = "black"
        bgcolor = "white"
        scaleFactor = 1
try:
    with open(config.file, 'r') as f:
        data = json.load(f)
        textinputStyle = data["textinput"]


        class TextInputStyles(Enum):

            try:
                margin = textinputStyle['margin']
            except Exception:
                margin = 10
            try:
                padding = textinputStyle['padding']
            except Exception:
                padding = 0
            try:
                color = textinputStyle['color']
            except Exception:
                color = "black"
            try:
                bordercolor = textinputStyle['bordercolor']
            except Exception:
                bordercolor = "black"
            try:
                anchor = textinputStyle['anchor']
            except Exception:
                anchor = "nw"
            try:
                borderWidth = textinputStyle['borderwidth']
            except Exception:
                borderWidth = 1
            try:
                borderWidthFocus = textinputStyle['borderwidthfocus']
            except Exception:
                borderWidthFocus = 5
except Exception:
    class TextInputStyles(Enum):
        margin = 10
        padding = 0
        bordercolor = "black"
        bgcolor = "grey"
        bgcolorHover = "light grey"
        anchor = "nw"
        color = "black"
        borderWidth = 5
        borderWidthFocus = 5