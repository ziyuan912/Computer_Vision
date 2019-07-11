from PIL import Image
import numpy as np
import math

img = (Image.open("lena.bmp")).convert("L")
w, h = img.size
mask = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
robert = Image.new("1", (w, h))
for i in range(w-1):
	for j in range(h-1):
		r1 = img.getpixel((i + 1,j + 1)) - img.getpixel((i,j))
		r2 = img.getpixel((i + 1,j)) - img.getpixel((i,j + 1))
		gradiant = math.sqrt(r1*r1 + r2*r2)
		if gradiant > 12:
			robert.putpixel((i,j),1)
		else:
			robert.putpixel((i,j),0)
robert.save('robert.bmp')

prewitt = Image.new("1", (w,h))
sobel = Image.new("1", (w,h))
frei_and_chen = Image.new("1", (w,h))
for i in range(1,w-1):
	for j in range(1,h-1):
		p = [0 for n in range(9)]
		for k in range(9):
			p[k] =  img.getpixel((i + mask[k][0],j + mask[k][1]))
		gradiantp = abs((p[6] + p[7] + p[8]) - (p[0] + p[1] + p[2])) + abs((p[2] + p[5] + p[8]) - (p[0] + p[3] + p[6]))
		gradiants = abs((p[6] + 2*p[7] + p[8]) - (p[0] + 2*p[1] + p[2])) + abs((p[2] + 2*p[5] + p[8]) - (p[0] + 2*p[3] + p[6]))
		f1 = (p[6] + math.sqrt(2)*p[7] + p[8]) - (p[0] + math.sqrt(2)*p[1] + p[2])
		f2 = (p[2] + math.sqrt(2)*p[5] + p[8]) - (p[0] + math.sqrt(2)*p[3] + p[6])
		gradiantf = math.sqrt(f1*f1 + f2*f2)
		if gradiantp > 24:
			prewitt.putpixel((i,j),1)
		else:
			prewitt.putpixel((i,j),0)
		if gradiants > 38:
			sobel.putpixel((i,j),1)
		else:
			sobel.putpixel((i,j),0)
		if gradiantf > 30:
			frei_and_chen.putpixel((i,j),1)
		else:
			frei_and_chen.putpixel((i,j),0)
prewitt.save('prewitt.bmp')
sobel.save('sobel.bmp')
frei_and_chen.save('frei_and_chen.bmp')

kirsch = Image.new("1", (w,h))
for i in range(1,w-1):
	for j in range(1,h-1):
		p = [0 for n in range(9)]
		kinitial = 0
		k = [0 for n in range(8)]
		for kk in range(9):
			p[kk] =  img.getpixel((i + mask[kk][0],j + mask[kk][1]))
			if kk != 4:
				kinitial += -3*p[kk]
		k[0] = kinitial + 8*(p[2] + p[5] + p[8])
		k[1] = kinitial + 8*(p[1] + p[2] + p[5])
		k[2] = kinitial + 8*(p[0] + p[1] + p[2])
		k[3] = kinitial + 8*(p[0] + p[1] + p[3])
		k[4] = kinitial + 8*(p[0] + p[3] + p[6])
		k[5] = kinitial + 8*(p[3] + p[6] + p[7])
		k[6] = kinitial + 8*(p[6] + p[7] + p[8])
		k[7] = kinitial + 8*(p[5] + p[7] + p[8])
		gradiantk = max(k)
		if gradiantk > 135:
			kirsch.putpixel((i,j),1)
		else:
			kirsch.putpixel((i,j),0)
kirsch.save('kirsch.bmp')

robinson = Image.new("1", (w,h))
for i in range(1,w-1):
	for j in range(1,h-1):
		p = [0 for n in range(9)]
		r = [0 for n in range(4)]
		for k in range(9):
			p[k] =  img.getpixel((i + mask[k][0],j + mask[k][1]))
		r[0] = abs((p[2] + 2*p[5] + p[8]) - (p[0] + 2*p[3] + p[6]))
		r[1] = abs((p[1] + 2*p[2] + p[5]) - (p[3] + 2*p[6] + p[7]))
		r[2] = abs((p[0] + 2*p[1] + p[2]) - (p[6] + 2*p[7] + p[8]))
		r[3] = abs((p[3] + 2*p[0] + p[1]) - (p[5] + 2*p[8] + p[7]))
		gradiantr = max(r)
		if gradiantr > 43:
			robinson.putpixel((i,j),1)
		else:
			robinson.putpixel((i,j),0)
robinson.save('robinson.bmp')

nevatia_babu = Image.new("1", (w,h))
for i in range(2,w-2):
	for j in range(2,h-2):
		p = [0 for m in range(25)]
		n = [0 for m in range(6)]
		ninitial = 0
		nvertical = 0
		count = 0
		for k in range(-2,3):
			for l in range(-2,3):
				p[count] = img.getpixel((i + l,j + k))
				if k < 0:
					ninitial += 100*p[count]
				elif k > 0:
					ninitial -= 100*p[count]
				if l < 0:
					nvertical -= 100*p[count]
				elif l > 0:
					nvertical += 100*p[count]
				count += 1
		n[0] = ninitial
		n[1] = n[0] - 22*p[8] - 132*p[9] + 100*p[10] + 92*p[11] - 92*p[13] - 100*p[14] + 132*p[15] + 22*p[16]
		n[2] = n[1] - 68*p[3] - 200*p[4] - 8*p[7] - 156*p[8] - 68*p[9] + 8*p[11] - 8*p[13] + 68*p[15] + 156*p[16] + 8*p[17] + 100*p[20] + 68*p[21]
		n[3] = nvertical
		n[4] = n[3] + 132*p[1] + 100*p[2] + 22*p[6] + 92*p[7] - 92*p[17] - 22*p[18] - 100*p[22] -132*p[23]
		n[5] = n[0] - 132*p[5] - 22*p[6] - 100*p[10] - 92*p[11] + 92*p[13] + 100*p[14] + 22*p[18] + 132*p[19]
		gradiantn = max(n)
		#print(gradiantn)
		if gradiantn > 12500:
			nevatia_babu.putpixel((i,j),1)
		else:
			nevatia_babu.putpixel((i,j),0)
nevatia_babu.save('nevatia_babu.bmp')  
