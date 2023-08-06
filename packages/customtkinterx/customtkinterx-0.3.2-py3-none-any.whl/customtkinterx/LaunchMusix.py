from tkinter import *
from tkinter import ttk
from customtkinter import *
from customtkinterx import *
import customtkinter
from typing import Union, Callable



def run_v1():
    from sys import platform

    CTkOffice2019Theme()

    set_appearance_mode("system")

    tk_root = CTkCustom()
    tk_root.create_sizegrip()
    tk_root.wm_geometry(f"350x620")

    tk_root.title("Musix.Py")
    tk_root.titlebar_title.configure(text="Musix.Py")

    frame_search = CTkFrame(tk_root.mainframe)
    combobox_search = CTkComboBox(frame_search, values=["Cloud Music"])
    combobox_search.set("Cloud Music")
    combobox_search.pack(fill="x", side="top", padx=5, pady=5)
    var_search = StringVar(value="Hopes And Dreams")
    entry_search = CTkEntry(frame_search, textvariable=var_search)
    entry_search.pack(side="left", fill="x", expand=True, padx=(5, 2.5), pady=5)
    switch_search = CTkSwitch(frame_search, text="Download", width=60)
    switch_search.pack(side="right", padx=(2.5, 5), pady=5)
    button_search = CTkButton(frame_search, text="Search", width=60)
    button_search.pack(side="right", padx=(2.5, 5), pady=5)
    frame_search.pack(fill="x", side="top", padx=5, pady=(5, 2.5))

    frame_results = CTkScrollableFrame(tk_root.mainframe)
    frame_results.pack(fill="both", expand="yes", padx=5, pady=(2.5, 5))


    def cloud_search():
        def _search():
            try:
                from cloudmusic import search, getMusic
            except ModuleNotFoundError:
                from os import system
                from sys import executable
                from threading import Thread


                Thread(target=lambda: system(f"{executable} -m pip install cloudmusic")).start()

            results = search(entry_search.get(), 15)
            for index in results:
                print(index.name)
                __ = index

                __frame = CTkFrame(frame_results)
                __frame.setvar()
                __frame.pack(fill="x", padx=2.5, pady=2.5, ipadx=5, ipady=5)
                CTkLabel(__frame, text=index.name).pack(side="left", fill="x", padx=5, pady=2.5)
                CTkLabel(__frame, text=index.id).pack(side="right", padx=5, pady=2.5)
                CTkLabel(__frame, text=','.join(index.artist)).pack(side="right", padx=5, pady=2.5)

                if switch_search.get():
                    __.download()

        from threading import Thread
        _search()


    def search():
        for index in frame_results.winfo_children(): index.destroy()
        if combobox_search.get() == "Cloud Music": cloud_search()


    button_search.configure(command=search)

    tk_root.mainloop()


def run_v2():
    class Spinbox(customtkinter.CTkFrame):
        def __init__(self, *args,
                     width: int = 100,
                     height: int = 32,
                     step_size: Union[int, float] = 1,
                     command: Callable = None,
                     **kwargs):
            super().__init__(*args, width=width, height=height, **kwargs)

            self.step_size = step_size
            self.command = command

            self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
            self.grid_columnconfigure(1, weight=1)  # entry expands

            self.subtract_button = customtkinter.CTkButton(self, text="-", width=height - 6, height=height - 6,
                                                           command=self.subtract_button_callback)
            self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

            self.entry = customtkinter.CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0)
            self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

            self.add_button = customtkinter.CTkButton(self, text="+", width=height - 6, height=height - 6,
                                                      command=self.add_button_callback)
            self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

            # default value
            self.entry.insert(0, "0")

        def add_button_callback(self):
            if self.command is not None:
                self.command()
            try:
                value = int(self.entry.get()) + self.step_size
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
            except ValueError:
                return

        def subtract_button_callback(self):
            if self.command is not None:
                self.command()
            try:
                value = int(self.entry.get()) - self.step_size
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
            except ValueError:
                return

        def get(self) -> Union[float, None]:
            try:
                return int(self.entry.get())
            except ValueError:
                return None

        def set(self, value: float):
            self.entry.delete(0, "end")
            self.entry.insert(0, str(int(value)))

    class MusicItem(CTkFrame):
        def __init__(self, master: any, music, **kwargs):
            super().__init__(master, **kwargs)

            self._fg_color = master._parent_frame._fg_color

            self._draw()

            self.music = music

            name: str = self.music.name + " - " + ','.join(self.music.artist)
            if len(name) >= 50:
                name = name[:48]+".."

            self.name = CTkLabel(self, text=name)
            self.name.pack(side="left", padx=5, pady=5)

            def download():
                self.music.download(level=self.args.get())

            self.bind("<Double-Button-1>", lambda event: download())

            self.download = CTkButton(self, width=100, text="下载", command=download)
            self.download.pack(side="right", padx=5, pady=5)

            self.args = CTkComboBox(self, values=["standard", "higher", "exhigh", "lossless"])
            self.args.set("higher")
            self.args.pack(side="right", padx=5, pady=5)

    CTkFluentAndroidTheme()
    set_appearance_mode("Light")

    root = CTkCustom(title="Musix")
    root.titlebar.configure(corner_radius=13)
    root.geometry("720x360")

    from sys import platform

    if platform == "win32":
        root.create_sizegrip(True)
        root.sizegrip.configure(text="", width=20, height=20, border_width=1)
    else:
        root.create_sizegrip(False)

    from PIL import Image

    root.titlebar_title.destroy()

    icon = CTkImage(light_image=Image.open("Musix.png"), dark_image=Image.open("Musix-Dark.png"), size=(30, 30))
    iconlabel = CTkLabel(root.titlebar, image=icon, text="", width=30, height=30)
    iconlabel.pack(side="left", padx=5, pady=5)

    title = CTkLabel(root.titlebar, text=root.title())
    title.pack(side="left", anchor="w", padx=10, pady=5)
    root.bind_move(title)

    version = CTkLabel(root.titlebar, text="v2.2.0", font=CTkFont(size=10))
    version.pack(side="left", anchor="sw", padx=10, pady=5)
    root.bind_move(version)

    info = CTkInfoBar(root.mainframe, title="公告", text="当前版本为重制版2.0，已是最新版本", severity=SUCCESS, can_close=False)
    info.show()

    def dark():
        if darkbox.get():
            set_appearance_mode("Dark")
        else:
            set_appearance_mode("Light")

    darkbox = CTkSwitch(info, text="启用深色主题", width=50, height=30, command=dark)
    darkbox.pack(side="right", padx=5, pady=5)

    numberbox = Spinbox(info, width=100, height=30)
    numberbox.set(15)
    numberbox.pack(side="right", padx=5, pady=5)

    musicbox = CTkScrollableFrame(root.mainframe)
    musicbox.pack(fill="both", expand="yes", padx=5, pady=5)


    def search():
        def _search():
            try:
                from cloudmusic import search, getMusic
                from prettytable import PrettyTable
            except ModuleNotFoundError:
                from os import system
                from sys import executable
                from threading import Thread

                CTkInfoBar(root.mainframe, title="错误", text="缺少依赖库，待cloudmusic、prettytable库下载完成后重试", severity=CRITICAL).show()

                Thread(target=lambda: system(f"{executable} -m pip install cloudmusic")).start()
                Thread(target=lambda: system(f"{executable} -m pip install prettytable")).start()

            if not searchbox.get() == "":
                for index in musicbox.winfo_children():
                    index.destroy()
                results = search(searchbox.get(), numberbox.get())

                table = PrettyTable(['名称', "作者", 'ID'])

                mlist = []

                for music in results:
                    list = [music.name, ','.join(music.artist), music.id]
                    table.add_row(list)

                    MusicItem(musicbox, music).pack(fill="x", side="top", padx=5, pady=5, ipadx=3, ipady=3)

                    mlist.append(list)

                print(table)

        from threading import Thread
        Thread(target=_search).start()

    searchbutton = CTkButton(root.titlebar, text="搜索", width=30, height=30, command=search)
    searchbutton.pack(side="right", padx=5, pady=5)

    searchbox = CTkEntry(root.titlebar, width=200, height=30)
    searchbox.configure(placeholder_text="请输入歌曲名称 （按Enter键搜索）")
    searchbox.bind("<Return>", lambda event: search())
    searchbox.pack(side="right", fill="x", expand="yes", padx=(15, 5), pady=5)

    #set_widget_scaling(1.15)
    root.wm_iconphoto(False, PhotoImage(file="Musix.png"))
    root.mainloop()

def run():
    run_v2()


if __name__ == '__main__':
    run()