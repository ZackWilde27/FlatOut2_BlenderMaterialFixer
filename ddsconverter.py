from PIL import Image
from os import scandir

try:
    from tkinter import filedialog
except:
    from Tkinter import filedialog

filename = filedialog.askopenfilename(filetypes = (("DirectDrawSurface", "*.dds"), ("All files","*.*")))
if not filename:
    raise Exception("Cancelled.")


filename = filename[:filename.rindex("/")]
for i in scandir(filename):
    if i.name[-4:] == ".dds":
        im = Image.open(i.path, 'r', None)
        im.save(i.path[:-4] + ".png")

print("Done!")
