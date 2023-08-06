from customtkinter import *
from customtkinterx import *

CTkGhostSharkTheme()

set_appearance_mode("dark")

root = CTkCustom()
root.title("CustomTkinterX")
root.titlebar_title.configure(text="CustomTkinterX")
root.create_sizegrip(True)

CTkButton(root.mainframe, text="Light", command=lambda: set_appearance_mode("light")).pack(fill="x", padx=5, pady=5, ipady=3)
CTkButton(root.mainframe, text="Dark", command=lambda: set_appearance_mode("dark")).pack(fill="x", padx=5, pady=5, ipady=3)

scrolledframe = CTkScrollableFrame(root.mainframe)
scrolledframe.pack(fill="both", expand="yes", padx=5, pady=5)

create_infobar = CTkButton(scrolledframe, command=lambda: CTkInfoBar(scrolledframe, severity=-1).show())
create_infobar.pack(side="top", fill="x", padx=5, pady=5, ipady=3)

root.mainloop()