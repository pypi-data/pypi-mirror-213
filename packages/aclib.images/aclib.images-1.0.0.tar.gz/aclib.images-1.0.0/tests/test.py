from aclib.images import Image

im = Image.fromcolor('ff0000', (222,333))
im.swapchannel().show()
