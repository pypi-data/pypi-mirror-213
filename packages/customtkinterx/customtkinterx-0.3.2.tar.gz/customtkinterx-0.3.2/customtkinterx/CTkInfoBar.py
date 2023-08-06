from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkFont, FontManager, ThemeManager, get_appearance_mode


NORMAL = "normal"
SUCCESS = "success"
CAUTION = "caution"
CRITICAL = "critical"


class CTkInfoBar(CTkFrame):
    def __init__(self, master=None,
                 corner_radius: int | str | None = None,
                 border_width: int | str | None = 0,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = None,
                 border_color: str | tuple[str, str] | None = None,

                 title: str = "CTkInfoBar",
                 text: str = "Info",

                 severity: str | int = "normal",

                 can_close: bool = True,

                 bell: bool = False,

                 **kwargs):
        super().__init__(master, bg_color=bg_color, border_width=border_width, corner_radius=corner_radius, **kwargs)

        if bell:
            self.bell()

        if severity == 0:
            severity = NORMAL
        elif severity == 1:
            severity = SUCCESS
        elif severity == 2:
            severity = CAUTION
        elif severity == 3:
            severity = CRITICAL
        elif severity == -1:
            from random import randint
            __r = randint(0, 3)

            if __r == 0:
                severity = NORMAL
            elif __r == 1:
                severity = SUCCESS
            elif __r == 2:
                severity = CAUTION
            elif __r == 3:
                severity = CRITICAL

        if "CTkInfoBar" in ThemeManager.theme:
            if fg_color is None:
                if severity == NORMAL:
                    self._fg_color = ThemeManager.theme["CTkInfoBar"]["fg_color"]
                elif severity == SUCCESS:
                    self._fg_color = ThemeManager.theme["CTkInfoBar"]["success_color"]
                elif severity == CAUTION:
                    self._fg_color = ThemeManager.theme["CTkInfoBar"]["caution_color"]
                elif severity == CRITICAL:
                    self._fg_color = ThemeManager.theme["CTkInfoBar"]["critical_color"]
            elif border_color is None:
                self._border_color = ThemeManager.theme["CTkInfoBar"]["border_color"]

        self.__label_title = CTkLabel(self, text=title, font=CTkFont(weight="bold"), anchor="w")
        self.__label_title.pack(fill="y", padx=(8, 4), pady=8, side="left")

        self.__label_info = CTkLabel(self, text=text, anchor="w")

        self.__label_info.pack(fill="y", padx=(4, 8), pady=8, side="left")

        self.__button_close = CTkButton(self, border_width=0, width=30, height=30, text="✕",
                                        command=lambda: self.destroy())

        self.configure(can_close=can_close)

        if "CTkInfoBar" in ThemeManager.theme:
            if fg_color is None:
                if severity == NORMAL:
                    self.__button_close._fg_color = ThemeManager.theme["CTkInfoBar"]["fg_color"]
                    self.__button_close._hover_color = ThemeManager.theme["CTkInfoBar"]["fg_hover_color"]
                    self.__button_close._text_color = ["#000000", "#ffffff"]
                elif severity == SUCCESS:
                    self.__button_close._fg_color = ThemeManager.theme["CTkInfoBar"]["success_color"]
                    self.__button_close._hover_color = ThemeManager.theme["CTkInfoBar"]["success_hover_color"]
                    self.__button_close._text_color = ["#000000", "#ffffff"]
                elif severity == CAUTION:
                    self.__button_close._fg_color = ThemeManager.theme["CTkInfoBar"]["caution_color"]
                    self.__button_close._hover_color = ThemeManager.theme["CTkInfoBar"]["caution_hover_color"]
                    self.__button_close._text_color = ["#000000", "#ffffff"]
                elif severity == CRITICAL:
                    self.__button_close._fg_color = ThemeManager.theme["CTkInfoBar"]["critical_color"]
                    self.__button_close._hover_color = ThemeManager.theme["CTkInfoBar"]["critical_hover_color"]
                    self.__button_close._text_color = ["#000000", "#ffffff"]

        self._draw()
        self.__button_close._draw()

    @property
    def title(self):
        return self.__label_title

    @property
    def info(self):
        return self.__label_info

    @property
    def close(self):
        return self.__button_close

    def configure(self, require_redraw=False, **kwargs):
        if "text" in kwargs:
            self.__label_info.configure(text=kwargs.pop("text"))
        elif "can_close" in kwargs:
            if kwargs.pop("can_close"):
                self.__button_close.pack(padx=8, pady=8, side="right", anchor="se")
            else:
                self.__button_close.pack_forget()

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self.__label_info.cget("text")
        else:
            return super().cget(attribute_name)

    def show(self, **kwargs):
        self.pack_configure(side="top", fill="x", ipadx=1, ipady=1, padx=5, pady=5)
        self.pack(**kwargs)


if __name__ == '__main__':
    from customtkinterx import CTkCustom, CTkFluentTheme
    from customtkinter import set_appearance_mode, CTkButton

    CTkFluentTheme()

    root = CTkCustom()
    root.create_sizegrip()

    set_appearance_mode("system")

    CTkInfoBar(root.mainframe, text="hello, i am a infobar", severity=NORMAL).show()
    CTkInfoBar(root.mainframe, text="hello, i am a infobar", severity=SUCCESS).show()
    CTkInfoBar(root.mainframe, text="hello, i am a infobar", severity=CAUTION).show()
    CTkInfoBar(root.mainframe, text="hello, i am a infobar", severity=CRITICAL).show()
    """
    CTkButton(root.mainframe, text="Light", command=lambda: set_appearance_mode("light")).pack(fill="x", padx=5, pady=5)
    CTkButton(root.mainframe, text="Dark", command=lambda: set_appearance_mode("dark")).pack(fill="x", padx=5, pady=5)
    """
    root.mainloop()