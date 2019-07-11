from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def dilation(imagein, pixel, kernal, w, h):
	maxval = 0
	for x in kernal:
		x2 = pixel[0] + x[0]
		y2 = pixel[1] + x[1]
		if 0 <= x2 < w and 0 <= y2 < h and imagein.getpixel((x2,y2)) > maxval:
			maxval = imagein.getpixel((x2,y2))
	return maxval

def erosion(imagein, pixel, kernal, w, h):
	minval = 255
	for x in kernal:
		x2 = pixel[0] + x[0]
		y2 = pixel[1] + x[1]
		if 0 <= x2 < w and 0 <= y2 < h and imagein.getpixel((x2,y2)) < minval:
			minval = imagein.getpixel((x2,y2))
	return minval

img = (Image.open("lena.bmp")).convert("L")
w, h = img.size
imgdilation = (Image.open("lena.bmp")).convert("L")
imgerosion = (Image.open("lena.bmp")).convert("L")
imgopen = (Image.open("lena.bmp")).convert("L")
imgclose = (Image.open("lena.bmp")).convert("L")
octogonal = [(0,0), (0,1), (0,2), (0,-1), (0,-2), (1,0), (1,1), (1,2), (1,-1), (1,-2), (2,0), (2,1), (2,-1), (-1,0), (-1,1), (-1,2), (-1,-1), (-1,-2), (-2,0), (-2,1), (-2,-1)]
for i in range(w):
	for j in range(h):
		maxval = dilation(img, (i,j), octogonal, w, h)
		imgdilation.putpixel((i,j), maxval)
		imgclose.putpixel((i,j), maxval)
		minval = erosion(img, (i,j), octogonal, w, h)
		imgerosion.putpixel((i,j), minval)
		imgopen.putpixel((i,j), minval)
imgdilation.save("dilation.bmp")
imgerosion.save("erosion.bmp")

#open and close
for i in range(w):
	for j in range(h):
		maxval = dilation(imgerosion, (i,j), octogonal, w, h)
		imgopen.putpixel((i,j), maxval)
		minval = erosion(imgdilation, (i,j), octogonal, w, h)
		imgclose.putpixel((i,j), minval)
imgopen.save("open.bmp")
imgclose.save("close.bmp")
