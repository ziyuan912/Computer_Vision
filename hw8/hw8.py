from PIL import Image
import numpy as np
import math


def Gaussian(img, img2, amp, w, h):
	for j in range(h):
		for i in range(w):
			gaus = img.getpixel((i,j)) + amp*np.random.normal(0,1,None)
			img2.putpixel((i,j),int(gaus))
	return 

def Salt(img, img2, threshold, w, h):
	for j in range(h):
		for i in range(w):
			if np.random.uniform(0,1,None) < threshold:
				salt = 0
			elif np.random.uniform(0,1,None) > 1-threshold:
				salt = 255
			else:
				salt = img.getpixel((i,j))
			img2.putpixel((i,j),salt)
	return 

def Box(img, img2, filtersize, w, h):
	move = (filtersize-1)/2
	for j in range(h):
		for i in range(w):
			pixelsum = 0
			for x in range(int(-1*move), int(move) + 1):
				for y in range(int(-1*move), int(move) + 1):
					#print(x,y)
					ii = i + x
					jj = j + y
					if 0 <= ii < w and 0 <= jj < h:
						pixelsum += img.getpixel((ii,jj))
			img2.putpixel((i,j), int(pixelsum/(filtersize*filtersize)))
	return 

def Median(img, img2, filtersize, w, h):
	move = (filtersize-1)/2
	for j in range(h):
		for i in range(w):
			plist = []
			for x in range(int(-1*move), int(move) + 1):
				for y in range(int(-1*move), int(move) + 1):
					#print(x,y)
					ii = i + x
					jj = j + y
					if 0 <= ii < w and 0 <= jj < h:
						plist.append(img.getpixel((ii,jj)))
					else:
						plist.append(0)
			img2.putpixel((i,j), int(np.median(plist)))
	return 

octogonal = [(0,0), (0,1), (0,2), (0,-1), (0,-2), (1,0), (1,1), (1,2), (1,-1), (1,-2), (2,0), (2,1), (2,-1), (-1,0), (-1,1), (-1,2), (-1,-1), (-1,-2), (-2,0), (-2,1), (-2,-1)]
def dilation(img, kernal, w, h, state):
	dil = np.zeros((w,h))
	for j in range(h):
		for i in range(w):
			maxpixel = 0
			for x in kernal:
				x2 = i + x[0]
				y2 = j + x[1]
				if 0 <= x2 < w and 0 <= y2 < h:
					if state == 1:
						pix = img.getpixel((x2,y2))
					else:
						pix = img[x2][y2]
					if pix > maxpixel:
						maxpixel = pix					
			dil[i][j] = maxpixel
	return dil
def erosion(img, kernal, w, h, state):
	ero = np.zeros((w,h))
	for j in range(h):
		for i in range(w):
			minpixel = 255
			for x in kernal:
				x2 = i + x[0]
				y2 = j + x[1]
				if 0 <= x2 < w and 0 <= y2 < h:
					if state == 1:
						pix = img.getpixel((x2,y2))
					else:
						pix = img[x2][y2]				
					if pix < minpixel:
						minpixel = pix
			ero[i][j] = minpixel
	return ero

def open(img, kernal, w, h, state):
	ero = erosion(img, kernal, w, h, state)
	opens = dilation(ero, kernal, w, h, 0)
	return opens
def close(img, kernal, w, h, state):
	dil = dilation(img, kernal, w, h, state)
	closes = erosion(dil, kernal, w, h, 0)
	return closes

def snr(origin, noise):
	w,h = origin.size
	vs = 0
	mu = 0
	vn = 0
	mun = 0
	snrr = 0
	for i in range(w):
		for j in range(h):
			mu += origin.getpixel((i,j))
			mun += noise.getpixel((i,j)) - origin.getpixel((i,j))
	mu /= w*h
	mun /= w*h
	for j in range(w):
		for i in range(h):
			vs += (origin.getpixel((i,j))-mu)*(origin.getpixel((i,j))-mu)
			vn += (noise.getpixel((i,j)) - origin.getpixel((i,j)) - mun)*(noise.getpixel((i,j)) - origin.getpixel((i,j)) - mun)
	vs /= w*h
	vn /= w*h
	snrr = 20*math.log(math.sqrt(vs)/math.sqrt(vn),10)
	return snrr



img = (Image.open("lena.bmp")).convert("L")
w, h = img.size

#4 noise figure
imgaussian10 = (Image.open("lena.bmp")).convert("L")
imgaussian30 = (Image.open("lena.bmp")).convert("L")
imgsalt005 = (Image.open("lena.bmp")).convert("L")
imgsalt01 = (Image.open("lena.bmp")).convert("L")
Gaussian(img, imgaussian10, 10, w, h)
Gaussian(img, imgaussian30, 30, w, h)
Salt(img, imgsalt005, 0.05, w, h)
Salt(img, imgsalt01, 0.1, w, h)
imgaussian10.save('gaussian10.bmp')
imgaussian30.save('gaussian30.bmp')
imgsalt01.save('salt01.bmp')
imgsalt005.save('salt005.bmp')
print("gaussian10: ", snr(img, imgaussian10))
print("gaussian30: ", snr(img, imgaussian30))
print("salt005: ", snr(img, imgsalt005))
print("salt01: ", snr(img, imgsalt01))

#box filter
imgbox3x3_gauss10 = (Image.open("lena.bmp")).convert("L")
imgbox3x3_gauss30 = (Image.open("lena.bmp")).convert("L")
imgbox3x3_salt005 = (Image.open("lena.bmp")).convert("L")
imgbox3x3_salt01 = (Image.open("lena.bmp")).convert("L")
imgbox5x5_gauss10 = (Image.open("lena.bmp")).convert("L")
imgbox5x5_gauss30 = (Image.open("lena.bmp")).convert("L")
imgbox5x5_salt005 = (Image.open("lena.bmp")).convert("L")
imgbox5x5_salt01 = (Image.open("lena.bmp")).convert("L")
Box(imgaussian10, imgbox3x3_gauss10, 3, w, h)
imgbox3x3_gauss10.save('box3x3_guassian10.bmp')
Box(imgaussian30, imgbox3x3_gauss30, 3, w, h)
imgbox3x3_gauss30.save('box3x3_guassian30.bmp')
Box(imgsalt005, imgbox3x3_salt005, 3, w, h)
imgbox3x3_salt005.save('box3x3_salt005.bmp')
Box(imgsalt01, imgbox3x3_salt01, 3, w, h)
imgbox3x3_salt01.save('box3x3_salt01.bmp')
Box(imgaussian10, imgbox5x5_gauss10, 5, w, h)
imgbox5x5_gauss10.save('box5x5_guassian10.bmp')
Box(imgaussian30, imgbox5x5_gauss30, 5, w, h)
imgbox5x5_gauss30.save('box5x5_guassian30.bmp')
Box(imgsalt005, imgbox5x5_salt005, 5, w, h)
imgbox5x5_salt005.save('box5x5_salt005.bmp')
Box(imgsalt01, imgbox5x5_salt01, 5, w, h)
imgbox5x5_salt01.save('box5x5_salt01.bmp')
print("box3x3_guassian10: ", snr(img, imgbox3x3_gauss10))
print("box3x3_guassian30: ", snr(img, imgbox3x3_gauss30))
print("box3x3_salt005: ", snr(img, imgbox3x3_salt005))
print("box3x3_salt01: ", snr(img, imgbox3x3_salt01))
print("box5x5_guassian10: ", snr(img, imgbox5x5_gauss10))
print("box5x5_guassian30: ", snr(img, imgbox5x5_gauss30))
print("box5x5_salt005: ", snr(img, imgbox5x5_salt005))
print("box5x5_salt01: ", snr(img, imgbox5x5_salt01))

#median filter
imgmedian3x3_gauss10 = (Image.open("lena.bmp")).convert("L")
imgmedian3x3_gauss30 = (Image.open("lena.bmp")).convert("L")
imgmedian3x3_salt005 = (Image.open("lena.bmp")).convert("L")
imgmedian3x3_salt01 = (Image.open("lena.bmp")).convert("L")
imgmedian5x5_gauss10 = (Image.open("lena.bmp")).convert("L")
imgmedian5x5_gauss30 = (Image.open("lena.bmp")).convert("L")
imgmedian5x5_salt005 = (Image.open("lena.bmp")).convert("L")
imgmedian5x5_salt01 = (Image.open("lena.bmp")).convert("L")
Median(imgaussian10, imgmedian3x3_gauss10, 3, w, h)
imgmedian3x3_gauss10.save('median3x3_gauss10.bmp')
Median(imgaussian30, imgmedian3x3_gauss30, 3, w, h)
imgmedian3x3_gauss30.save('median3x3_guassian30.bmp')
Median(imgsalt005, imgmedian3x3_salt005, 3, w, h)
imgmedian3x3_salt005.save('median3x3_salt005.bmp')
Median(imgsalt01, imgmedian3x3_salt01, 3, w, h)
imgmedian3x3_salt01.save('median3x3_salt01.bmp')
Median(imgaussian10, imgmedian5x5_gauss10, 5, w, h)
imgmedian5x5_gauss10.save('median5x5_guassian10.bmp')
Median(imgaussian30, imgmedian5x5_gauss30, 5, w, h)
imgmedian5x5_gauss30.save('median5x5_guassian30.bmp')
Median(imgsalt005, imgmedian5x5_salt005, 5, w, h)
imgmedian5x5_salt005.save('median5x5_salt005.bmp')
Median(imgsalt01, imgmedian5x5_salt01, 5, w, h)
imgmedian5x5_salt01.save('median5x5_salt01.bmp')
print("median3x3_guassian10: ", snr(img, imgmedian3x3_gauss10))
print("median3x3_guassian30: ", snr(img, imgmedian3x3_gauss30))
print("median3x3_salt005: ", snr(img, imgmedian3x3_salt005))
print("median3x3_salt01: ", snr(img, imgmedian3x3_salt01))
print("median5x5_guassian10: ", snr(img, imgmedian5x5_gauss10))
print("median5x5_guassian30: ", snr(img, imgmedian5x5_gauss30))
print("median5x5_salt005: ", snr(img, imgmedian5x5_salt005))
print("median5x5_salt01: ", snr(img, imgmedian5x5_salt01))
#open and close
imgopenclose_guass10 = (Image.open("gaussian10.bmp")).convert("L")
imgopenclose_guass30 = (Image.open("gaussian10.bmp")).convert("L")
imgopenclose_salt005 = (Image.open("gaussian10.bmp")).convert("L")
imgopenclose_salt01 = (Image.open("gaussian10.bmp")).convert("L")
imgcloseopen_guass10 = (Image.open("gaussian10.bmp")).convert("L")
imgcloseopen_guass30 = (Image.open("gaussian10.bmp")).convert("L")
imgcloseopen_salt005 = (Image.open("gaussian10.bmp")).convert("L")
imgcloseopen_salt01 = (Image.open("gaussian10.bmp")).convert("L")
openclose = []
closeopen = []
openclose.append(close(open(imgaussian10, octogonal, w, h, 1), octogonal, w, h, 0))
openclose.append(close(open(imgaussian30, octogonal, w, h, 1), octogonal, w, h, 0))
openclose.append(close(open(imgsalt005, octogonal, w, h, 1), octogonal, w, h, 0))
openclose.append(close(open(imgsalt01, octogonal, w, h, 1), octogonal, w, h, 0))
closeopen.append(open(close(imgaussian10, octogonal, w, h, 1), octogonal, w, h, 0))
closeopen.append(open(close(imgaussian30, octogonal, w, h, 1), octogonal, w, h, 0))
closeopen.append(open(close(imgsalt005, octogonal, w, h, 1), octogonal, w, h, 0))
closeopen.append(open(close(imgsalt01, octogonal, w, h, 1), octogonal, w, h, 0))
for i in range(w):
	for j in range(h):
		imgopenclose_guass10.putpixel((i,j), int(openclose[0][i][j]))
		imgopenclose_guass30.putpixel((i,j), int(openclose[1][i][j]))
		imgopenclose_salt005.putpixel((i,j), int(openclose[2][i][j]))
		imgopenclose_salt01.putpixel((i,j), int(openclose[3][i][j]))
		imgcloseopen_guass10.putpixel((i,j), int(closeopen[0][i][j]))
		imgcloseopen_guass30.putpixel((i,j), int(closeopen[1][i][j]))
		imgcloseopen_salt005.putpixel((i,j), int(closeopen[2][i][j]))
		imgcloseopen_salt01.putpixel((i,j), int(closeopen[3][i][j]))
imgopenclose_guass10.save('open_close_gaussian10.bmp')
imgopenclose_guass30.save('open_close_gaussian30.bmp')
imgopenclose_salt005.save('open_close_salt005.bmp')
imgopenclose_salt01.save('open_close_salt01.bmp')
imgcloseopen_guass10.save('close_open_gaussian10.bmp')
imgcloseopen_guass30.save('close_open_gaussian30.bmp')
imgcloseopen_salt005.save('close_open_salt005.bmp')
imgcloseopen_salt01.save('close_open_salt01.bmp')
print("open_close_gaussian10:", snr(img, imgopenclose_guass10))
print("open_close_gaussian30:", snr(img, imgopenclose_guass30))
print("open_close_salt005:", snr(img, imgopenclose_salt005))
print("open_close_salt01:", snr(img, imgopenclose_salt01))
print("close_open_gaussian10:", snr(img, imgcloseopen_guass10))
print("close_open_gaussian30:", snr(img, imgcloseopen_guass30))
print("close_open_salt005:", snr(img, imgcloseopen_salt005))
print("close_open_salt01:", snr(img, imgcloseopen_salt01))






