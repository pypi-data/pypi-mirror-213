import base64

open_file = open("HarmonyOS_Sans_Regular.ttf", "rb")
b64str = base64.b64encode(open_file.read())
open_file.close()
write_data = format(b64str)
f = open("output.txt", "w+")
f.write(write_data)  # 生成ASCII码
f.close()