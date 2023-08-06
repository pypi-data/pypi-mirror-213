from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton
from customtkinterx.fluent_android import CTkFluentAndroidTheme


class CTkFluentAppBar(CTkFrame):
    def __init__(self, master=None, *args, width=360, height=80, title: str = "Title", subtitle: str = "Subtitle", bg_color="#ffffff", **kwargs):
        super().__init__(master, *args, width=width, height=height, bg_color=bg_color, **kwargs)

        self.__title = CTkLabel(self, text=title, font=CTkFont(family="Roboto", size=15, weight="bold"))
        self.__title.pack(anchor="nw", padx=8, pady=(8, 0))

        self.__subtitle = CTkLabel(self, text=subtitle, font=CTkFont(family="Roboto", size=12, weight="normal"))
        self.__subtitle.pack(anchor="nw", padx=8, pady=(0, 8))

    def create_closebutton(self):
        __button = CTkButton(self)
        __button.pack(anchor="ne", side="top", padx=8, pady=8)
        return __button

    @property
    def title(self):
        return self.__title

    @property
    def subtitle(self):
        return self.__subtitle

    def show(self):
        self.pack(fill="x", side="top")


if __name__ == '__main__':
    from customtkinterx import CTkCustom
    from customtkinter import CTk, set_appearance_mode, set_widget_scaling

    set_appearance_mode("dark")

    CTkFluentAndroidTheme()

    root = CTkCustom()
    root.geometry("380x680")

    set_widget_scaling(1.2)

    root.titlebar.forget()
    root.create_sizegrip(False)

    appbar = CTkFluentAppBar(root.mainframe)
    root.bind_move(appbar)
    appbar.pack(fill="x", side="top", padx=1, pady=1)

    button1 = CTkButton(root.mainframe, width=90, height=38)
    button1.pack()

    root.mainloop()