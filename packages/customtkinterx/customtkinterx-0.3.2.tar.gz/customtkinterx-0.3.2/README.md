# CustomTkinterX
> 解释器需Python3.7及以上

`customtkinter`的扩展组件功能库，同时也采集了其他开发者制作的组件，并进行仅类型提示上的修改（源代码`__main__.py`上有标注）

## Fluent主题
尚未完善设置，修改了`CTk` `CTkToplevel` `CTkFrame` `CTkButton` `CTKEntry` `CTkComboBox`等类。
```python
from customtkinter import *
from customtkinterx import *

CTkFluentTheme()
```

## CTkCustom 自定义窗口
原窗口因标题栏与边框的限制，导致界面效果极差，但是仍可以通过一些方法自定义窗口`wm_overrideredirect`。
平台支持`Windows` `MacOS` `Linux`，其中界面效果支持最好的是`Windows`，`MacOS` `Linux`无法使用透明色，完全消除边框使用圆角，
及将图标保留至任务栏，采用置顶的方法保持窗口的显示。

### 组件结构
```markdown
| CTkCustom -> CTk
|-->> __frame_border(mainframe): CTkFrame
|-->> __frame_title(titlebar): CTkFrame
|-->> __label_title(titlebar_title): CTkLabel
|-->> __button_close(titlebar_closebutton): CTkButton
|-->> __button_minimize(titlebar_minimizebutton): CTkButton
```

### 基础示例
```python
from customtkinter import *
from customtkinterx import *

root = CTkCustom()

root.mainloop()
```

### 主题配置
你可以自定义一个主题，然后加上`CTkCustom`项
```json
{
  ...
    "transparent_color": "#101010", // 为实现圆角边框而设置的透明色

    "closebutton_text_color": ["#000000", "#ffffff"],
    "closebutton_color": ["#f4f6f8", "#212b36"],
    "closebutton_hover_color": ["#b40d1b", "#b40d1b"],

    "minimizebutton_text_color": ["#000000", "#ffffff"],
    "minimizebutton_color": ["#f4f6f8", "#212b36"],
    "minimizebutton_hover_color": ["#dfe3e8", "#454f5b"]
  },
  ...
}
```

### 添加缩放窗口大小的手柄
```python
CTKCustom.create_sizegrip()
```
自定义手柄，将会使用库`pyautogui`。
```bash
python -m pyautogui
```
```python
CTKCustom.create_sizegrip(True)
```

```python
from customtkinter import *
from customtkinterx import *

root = CTkCustom()
root.create_sizegrip()

root.mainloop()
```

```python
from customtkinter import *
from customtkinterx import *

root = CTkCustom()
root.create_sizegrip(True)

root.mainloop()
```

## CTkInfoBar 消息栏
### 组件结构
```markdown
| CTkInforBar -> CTkFrame
|-->> __label_title(title): CTkLabel
|-->> __label_info(info): CTkLabel
|-->> __button_close(close): CTkButton
```

### 基础示例
```python
from customtkinter import *
from customtkinterx import *

root = CTk()

infobar = CTkInfoBar()
infobar.show()

root.mainloop()
```

### 主题配置
你可以自定义一个主题，然后加上`CTkInfoBar`项
```json
{
  ...
  "CTkInfoBar": {
    "corner_radius": 8,
    "border_width": 0,

    "fg_color": ["#61f3f3", "#006c9c"], 
    "fg_hover_color": ["#cafdf5", "#003768"], // 关闭按钮被鼠标捕捉时的颜色

    "border_color": ["#b0b2b2", "#424556"],  

    "success_color": ["#86e8ab", "#1b806a"],  // 取自配色severity中NORMAL值
    "success_hover_color": ["#d8fbde", "#0a5554"],  // 取自配色severity中被鼠标捕捉时的NORMAL值
    "caution_color": ["#ffd666", "#b76e00"],  // 取自配色severity中CAUTION值
    "caution_hover_color": ["#fff5cc", "#7a4100"],  // 取自配色severity中被鼠标捕捉时的CAUTION值
    "critical_color": ["#ffac82", "#b71d18"],  // 取自配色severity中CRITICAL值
    "critical_hover_color": ["#ffe9d5", "#7a0916"]  // 取自配色severity中被鼠标捕捉时的CAUTION值

  },
  ...
}
```