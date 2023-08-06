minimal_json = """
{
  "CTkCustom": {
    "titlebar_color": ["#f4f6f8", "#212b36"],
    "title_color": ["gray10", "#DCE4EE"],

    "transparent_color": "#101010",

    "closebutton_text_color": ["#000000", "#ffffff"],
    "closebutton_color": ["#f4f6f8", "#212b36"],
    "closebutton_hover_color": ["#b40d1b", "#b40d1b"],

    "minimizebutton_text_color": ["#000000", "#ffffff"],
    "minimizebutton_color": ["#f4f6f8", "#212b36"],
    "minimizebutton_hover_color": ["#dfe3e8", "#454f5b"]
  },
  "CTkInfoBar": {
    "corner_radius": 8,
    "border_width": 0,

    "fg_color": ["#61f3f3", "#006c9c"],
    "fg_hover_color": ["#cafdf5", "#003768"],

    "border_color": ["#b0b2b2", "#424556"],

    "success_color": ["#86e8ab", "#1b806a"],
    "success_hover_color": ["#d8fbde", "#0a5554"],
    "caution_color": ["#ffd666", "#b76e00"],
    "caution_hover_color": ["#fff5cc", "#7a4100"],
    "critical_color": ["#ffac82", "#b71d18"],
    "critical_hover_color": ["#ffe9d5", "#7a0916"]

  },
  "CTk": {
    "fg_color": ["#f9fafb", "#161c24"]
  },
  "CTkToplevel": {
    "fg_color": ["#f9fafb", "#161c24"]
  },
  "CTkFrame": {
    "corner_radius": 10,
    "border_width": 1,
    "fg_color": ["#f9fafb", "#161c24"],
    "top_fg_color": ["#f4f6f8", "#212b36"],
    "border_color": ["#edeff1", "#212b36"]
  },
  "CTkButton": {
    "corner_radius": 10,
    "border_width": 0,
    "fg_color": "#00ab55",
    "hover_color": "#007b55",
    "border_color": ["#f3f3f3", "#949A9F"],
    "text_color": ["#ffffff", "#000000"],
    "text_color_disabled": ["gray74", "gray60"]
  },
  "CTkLabel": {
    "corner_radius": 0,
    "fg_color": "transparent",
    "text_color": ["gray10", "#DCE4EE"]
  },
  "CTkEntry": {
    "corner_radius": 10,
    "border_width": 1,
    "fg_color": ["#dfe3e8", "#454f5b"],
    "border_color": ["#c4cdd5", "#637381"],
    "text_color":["#000000", "#ffffff"],
    "placeholder_text_color": ["gray52", "gray62"]
  },
  "CTkCheckbox": {
    "corner_radius": 6,
    "border_width": 3,
    "fg_color": ["#3B8ED0", "#1F6AA5"],
    "border_color": ["#3E454A", "#949A9F"],
    "hover_color": ["#3B8ED0", "#1F6AA5"],
    "checkmark_color": ["#DCE4EE", "gray90"],
    "text_color": ["gray10", "#DCE4EE"],
    "text_color_disabled": ["gray60", "gray45"]
  },
  "CTkSwitch": {
    "corner_radius": 1000,
    "border_width": 0,
    "button_length": 0,
    "fg_color": ["#c4cdd5", "#637381"],
    "progress_color": "#00ab55",
    "button_color": ["#f9fafb", "#161c24"],
    "button_hover_color": ["#f4f6f8", "#212b36"],
    "text_color": ["gray10", "#DCE4EE"],
    "text_color_disabled": ["gray60", "gray45"]
  },
  "CTkRadiobutton": {
    "corner_radius": 1000,
    "border_width_checked": 6,
    "border_width_unchecked": 3,
    "fg_color": ["#3B8ED0", "#1F6AA5"],
    "border_color": ["#3E454A", "#949A9F"],
    "hover_color": ["#36719F", "#144870"],
    "text_color": ["gray10", "#DCE4EE"],
    "text_color_disabled": ["gray60", "gray45"]
  },
  "CTkProgressBar": {
    "corner_radius": 1000,
    "border_width": 0,
    "fg_color": ["#939BA2", "#4A4D50"],
    "progress_color": ["#3B8ED0", "#1F6AA5"],
    "border_color": ["gray", "gray"]
  },
  "CTkSlider": {
    "corner_radius": 1000,
    "button_corner_radius": 1000,
    "border_width": 6,
    "button_length": 0,
    "fg_color": ["#939BA2", "#4A4D50"],
    "progress_color": ["gray40", "#AAB0B5"],
    "button_color": ["#3B8ED0", "#1F6AA5"],
    "button_hover_color": ["#36719F", "#144870"]
  },
  "CTkOptionMenu": {
    "corner_radius": 6,
    "fg_color": ["#3B8ED0", "#1F6AA5"],
    "button_color": ["#36719F", "#144870"],
    "button_hover_color": ["#27577D", "#203A4F"],
    "text_color": ["#DCE4EE", "#DCE4EE"],
    "text_color_disabled": ["gray74", "gray60"]
  },
  "CTkComboBox": {
    "corner_radius": 10,
    "border_width": 1,
    "fg_color": ["#dfe3e8", "#454f5b"],
    "border_color": ["#c4cdd5", "#637381"],
    "button_color": ["#c4cdd5", "#637381"],
    "button_hover_color": ["#919eab", "#919eab"],
    "text_color": ["gray10", "#ffffff"],
    "text_color_disabled": ["gray50", "gray45"]
  },
  "CTkScrollbar": {
    "corner_radius": 1000,
    "border_spacing": 4,
    "fg_color": "transparent",
    "button_color": ["#f4f6f8", "#212b36"],
    "button_hover_color": ["#dfe3e8", "#454f5b"]
  },
  "CTkSegmentedButton": {
    "corner_radius": 6,
    "border_width": 2,
    "fg_color": ["#979DA2", "gray29"],
    "selected_color": ["#3B8ED0", "#1F6AA5"],
    "selected_hover_color": ["#36719F", "#144870"],
    "unselected_color": ["#979DA2", "gray29"],
    "unselected_hover_color": ["gray70", "gray41"],
    "text_color": ["#DCE4EE", "#DCE4EE"],
    "text_color_disabled": ["gray74", "gray60"]
  },
  "CTkTextbox": {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ["#dfe3e8", "#454f5b"],
    "border_color": ["#979DA2", "#565B5E"],
    "text_color":["gray10", "#DCE4EE"],
    "scrollbar_button_color": ["gray55", "gray41"],
    "scrollbar_button_hover_color": ["gray40", "gray53"]
  },
  "CTkScrollableFrame": {
    "label_fg_color": ["gray78", "gray23"]
  },
  "DropdownMenu": {
    "fg_color": ["gray90", "#1c1c1c"],
    "hover_color": ["gray75", "#313131"],
    "text_color": ["gray10", "#ffffff"]
  },
  "CTkFont": {
    "macOS": {
      "family": "SF Display",
      "size": 13,
      "weight": "normal"
    },
    "Windows": {
      "family": "Roboto",
      "size": 13,
      "weight": "normal"
    },
    "Linux": {
      "family": "Roboto",
      "size": 13,
      "weight": "normal"
    }
  }
}
"""


import os.path


minimal_path = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/") + "/Minimal.json"


def minimal_theme():
    from tempfile import mkstemp
    from customtkinter import set_default_color_theme
    _, __temp = mkstemp(suffix=".json")
    with open(__temp, "w") as __temp_file:
        __temp_file.write(minimal_json)
    return __temp


def use_minimal_theme():
    from customtkinter import set_default_color_theme
    try:
        set_default_color_theme(minimal_path)
    except FileNotFoundError:
        set_default_color_theme(minimal_theme())
