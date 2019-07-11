from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def dilation(image, pixel, kernal, w, h):
	for x in kernal:
		x2 = pixel[0] + x[0]
		y2 = pixel[1] + x[1]
		if 0 <= x2 < w and 0 <= y2 < h:
			image.putpixel((x2, y2), 1)
	return

def erosion(image, pixel, kernal, w, h):
	black = 0
	for x in octogonal:
		i2 = i + x[0]
		j2 = j + x[1]
		if 0 <= i2 < w and 0 <= j2 < h:
			if image.getpixel((i2,j2)) == 0:
				black = 1
				break
	if black == 1:
		return 0
	else:
		return 1

img = (Image.open("lena.bmp")).convert("L")
w, h = img.size
img2 = Image.new("1", (w,h))
imgdilation = Image.new("1", (w,h))
imgerosion = Image.new("1", (w,h))
imghitmiss = Image.new("1", (w,h))
imgopen = Image.new("1", (w,h))
imgclose = Image.new("1", (w,h))
octogonal = [(0,0), (0,1), (0,2), (0,-1), (0,-2), (1,0), (1,1), (1,2), (1,-1), (1,-2), (2,0), (2,1), (2,-1), (-1,0), (-1,1), (-1,2), (-1,-1), (-1,-2), (-2,0), (-2,1), (-2,-1)]
hit = [(0,0), (-1,0), (0,1)]
miss = [(1,-1), (1,0), (0,-1)]
for i in range(w):
	for j in range(h):
		if img.getpixel((i,j)) < 128:
			img2.putpixel((i, j), 0)
			imgdilation.putpixel((i,j), 0)
			imgerosion.putpixel((i, j), 0)
			imghitmiss.putpixel((i,j), 0)
			imgopen.putpixel((i,j), 0)
			imgclose.putpixel((i,j), 0)
		elif img.getpixel((i,j)) >= 128:
			img2.putpixel((i, j), 1)
			imgdilation.putpixel((i,j), 1)
			imgerosion.putpixel((i, j), 1)
			imghitmiss.putpixel((i,j), 1)
			imgopen.putpixel((i,j), 1)
			imgclose.putpixel((i,j), 1)
for i in range(w):
	for j in range(h):
		if img2.getpixel((i, j)) == 1:
			dilation(imgdilation, (i,j), octogonal, w, h)
			dilation(imgclose, (i,j), octogonal, w, h)
			erosions = erosion(img2, (i,j), octogonal, w, h)
			imgerosion.putpixel((i,j), erosions)
			imgopen.putpixel((i,j), erosions)
			#hit and miss
			black = 0
			for x in hit:
				i2 = i + x[0]
				j2 = j + x[1]
				if 0 <= i2 < w and 0 <= j2 < h:
					if img2.getpixel((i2,j2)) == 0:
						black = 1
			for x in miss:
				i2 = i + x[0]
				j2 = j + x[1]
				if 0 <= i2 < w and 0 <= j2 < h:
					if img2.getpixel((i2,j2)) == 1:
						black = 1
			if black == 1:
				imghitmiss.putpixel((i, j), 0)
imgdilation.save("dilation.bmp")
imgerosion.save("erosion.bmp")

#open and close
for i in range(w):
	for j in range(h):
		if imgerosion.getpixel((i,j)) == 1:
			dilation(imgopen, (i,j), octogonal, w, h)
		if imgdilation.getpixel((i,j)) == 1:
			erosions = erosion(imgdilation, (i,j), octogonal, w, h)
			imgclose.putpixel((i,j), erosions)

imghitmiss.save("hitmiss.bmp")
imgopen.save("open.bmp")
imgclose.save("close.bmp")
