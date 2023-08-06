"""
Customtkinter Menu Bar
Author: Akash Bora
"""

import customtkinter


class CTkMenuBar(customtkinter.CTkFrame):

    def __init__(
            self,
            master,
            bg_color=["white", "black"],
            height=25,
            width=10,
            padx=5,
            pady=2,
            **kwargs):

        if master.winfo_name().startswith("!ctkframe"):
            bg_corners = ["", "", bg_color, bg_color]
            corner = master.cget("corner_radius")
        else:
            bg_corners = ["", "", "", ""]
            corner = 0

        super().__init__(master, fg_color=bg_color, corner_radius=corner, height=height,
                         background_corner_colors=bg_corners, **kwargs)
        self.height = height
        self.width = width
        self.after(10)
        self.num = 0
        self.menu = []
        self.padx = padx
        self.pady = pady
        super().pack(anchor="n", fill="x")

    def add_cascade(self, text=None, **kwargs):

        if not "fg_color" in kwargs:
            fg_color = "transparent"
        else:
            fg_color = kwargs.pop("fg_color")
        if not "text_color" in kwargs:
            text_color = customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]
        else:
            text_color = kwargs.pop("text_color")

        if not "anchor" in kwargs:
            anchor = "w"
        else:
            anchor = kwargs.pop("anchor")

        if text is None:
            text = f"Menu {self.num + 1}"

        self.menu_button = customtkinter.CTkButton(self, text=text, fg_color=fg_color,
                                                   text_color=text_color, width=self.width,
                                                   height=self.height, anchor=anchor, **kwargs)
        self.menu_button.grid(row=0, column=self.num, padx=(self.padx, 0), pady=self.pady)
        self.num += 1

        return self.menu_button

    def configure(self, **kwargs):
        if "bg_color" in kwargs:
            self.configure(fg_color=kwargs.pop("bg_color"))
        self.configure(**kwargs)


if __name__ == '__main__':
    import customtkinter
    from customtkinterx.CTkMenuBar import *

    root = customtkinter.CTk()
    root.geometry("600x200")

    menu = CTkMenuBar(root)
    button_1 = menu.add_cascade("File")
    button_2 = menu.add_cascade("Edit")
    button_3 = menu.add_cascade("Settings")
    button_4 = menu.add_cascade("About")

    dropdown1 = CustomDropdownMenu(widget=button_1)
    dropdown1.add_option(option="Open", command=lambda: print("Open"))
    dropdown1.add_option(option="Save")

    dropdown1.add_separator()

    sub_menu = dropdown1.add_submenu("Export As")
    sub_menu.add_option(option=".TXT")
    sub_menu.add_option(option=".PDF")

    dropdown2 = CustomDropdownMenu(widget=button_2)
    dropdown2.add_option(option="Cut")
    dropdown2.add_option(option="Copy")
    dropdown2.add_option(option="Paste")

    dropdown3 = CustomDropdownMenu(widget=button_3)
    dropdown3.add_option(option="Preferences")
    dropdown3.add_option(option="Update")

    dropdown4 = CustomDropdownMenu(widget=button_4)
    dropdown4.add_option(option="Hello World")

    root.mainloop()
