from customtkinter import CTkFrame, ThemeManager, CTkLabel, CTkFont, CTkScrollableFrame, CTkButton, CTkToplevel
from customtkinterx import CTkCustom


class CTkMegaMenuBar(CTkFrame):
    def __init__(self, master=None, title: str = "Mega Menu", custom: CTkCustom = None, **kwargs):
        super().__init__(master, **kwargs)

        self.__custom = custom

        if self.__custom is not None:
            self.__label_title = CTkLabel(self.__custom.titlebar, text=title, anchor="w", font=CTkFont(weight="bold"))
            self.__label_title.pack(side="left", fill="y", padx=8, pady=5)
            self.__custom.bind_move(self.__label_title)

            self.__scrolledframe_menus = CTkScrollableFrame(self)
            self.__scrolledframe_menus.pack(fill="both", expand="yes", padx=5, pady=5)
        else:
            self.__label_title = CTkLabel(self, text=title, anchor="w", font=CTkFont(weight="bold"))
            self.__label_title.pack(side="top", fill="x", padx=8, pady=5)

            self.__scrolledframe_menus = CTkScrollableFrame(self)
            self.__scrolledframe_menus.pack(fill="both", expand="yes", padx=5, pady=5)

        self.__buttons = {}

    def show(self, **kwargs):
        self.pack(fill="y", side="left", padx=5, pady=5, ipadx=5, ipady=5)
        if self.__custom is not None:
            self.pack(padx=2, pady=0)
        self.pack_configure(**kwargs)

    def add(self, menu):
        menu.pack(fill="x", side="top", padx=0, pady=5, ipadx=5, ipady=5)

    @property
    def menus(self):
        return self.__buttons

    @property
    def title(self):
        return self.__label_title

    @property
    def menubar(self):
        return self.__scrolledframe_menus


class CTkMegaMenu(CTkButton):
    def __init__(self, master: CTkMegaMenuBar, text="Menu", width=30, **kwargs):
        super().__init__(master.menubar, width=width, text=text, anchor="w", **kwargs)

        self._fg_color = master._fg_color
        self._text_color = ThemeManager.theme["CTkLabel"]["text_color"]
        self._draw()


if __name__ == '__main__':
    from customtkinterx import CTkCustom, CTkMinimalTheme, CTkFluentTheme, CTkOffice2019Theme

    CTkOffice2019Theme()
    #CTkMinimalTheme()
    #CTkFluentTheme()

    root = CTkCustom(title="CTkMegaMenuBar")
    root.create_sizegrip()

    menubar = CTkMegaMenuBar(root.mainframe, custom=root)
    for menu in range(10):
        _menu = CTkMegaMenu(menubar, text="Menu"+str(menu))
        menubar.add(_menu)
    menubar.show()

    root.mainloop()