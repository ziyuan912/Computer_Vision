from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

img=(Image.open("lena.bmp")).convert("L")
w, h = img.size
pixel = [[None]*347 for i in range(348)]
img2 = Image.new("L", (w, h))
img3 = Image.new("L", (w, h))
img4 = Image.new("L", (w, h))
for i in range(w):
	for j in range(h):
		img2.putpixel((i, j), img.getpixel((i,h - j - 1)))
		img3.putpixel((i, j), img.getpixel((w - i - 1, j)))
		img4.putpixel((i, j), img.getpixel((w - i - 1,h - j - 1)))
img2.save("lena2.bmp")
img3.save("lena3.bmp")
img4.save("lena4.bmp")
