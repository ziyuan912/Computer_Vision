from PIL import Image
import numpy as np
import math

img = (Image.open("lena.bmp")).convert("L")
w, h = img.size
laplace1 = Image.new("1", (w, h))
laplace2 = Image.new("1", (w, h))
for i in range(1,w-1):
	for j in range(1,h-1):
		connect4 = 0
		connect8 = 0
		for k in range(-1,2):
			for l in range(-1,2):
				if (k == 0 or l == 0) and (k != l):
					connect4 += img.getpixel((i+l,j+k))
					connect8 += img.getpixel((i+l,j+k))
				elif (k,l) != (0,0):
					connect8 += img.getpixel((i+l,j+k))
		connect4 -= 4*img.getpixel((i,j))
		connect8 -= 8*img.getpixel((i,j))
		connect8 /= 3
		if connect4 > 15:
			laplace1.putpixel((i,j),0)
		else:
			laplace1.putpixel((i,j),1)
		if connect8 > 15:
			laplace2.putpixel((i,j),0)
		else:
			laplace2.putpixel((i,j),1)
laplace1.save('laplace1.bmp')
laplace2.save('laplace2.bmp')

minvarlaplace = Image.new("1", (w, h))
mask = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
for i in range(1,w-1):
	for j in range(1,h-1):
		p = [0 for i in range(9)]
		for k in range(9):
			p[k] =  img.getpixel((i + mask[k][0],j + mask[k][1]))
		minvar = 2*(p[0] + p[2] + p[6] + p[8]) - (p[1] + p[3] + p[5] + p[7]) - 4*p[4]
		minvar /= 3
		if minvar > 20:
			minvarlaplace.putpixel((i,j),0)
		else:
			minvarlaplace.putpixel((i,j),1)
minvarlaplace.save('minvarlaplace.bmp')

guassianlap = Image.new("1", (w,h))
differencelap = Image.new("1", (w,h))
for i in range(5,w-5):
	for j in range(5,h-5):
		p = [[0]*11 for i in range(11)]
		for k in range(11):
			for l in range(11):
				p[l][k] = img.getpixel((i+l-5,j+k-5))
		guassian = 178*p[5][5] + 103*(p[5][4] + p[5][6] + p[4][5] + p[6][5]) - 1*(p[5][3] + p[5][7] + p[3][5] + p[7][5]) - 23*(p[5][2] + p[2][5] + p[5][8] + p[8][5]) -9*(p[5][1] + p[1][5] + p[5][9] + p[9][5]) - 2*(p[5][0] + p[0][5] + p[5][10] + p[10][5]) + 52*(p[4][4] + p[6][4] + p[4][6] + p[6][6]) -14*(p[4][3] + p[3][4] + p[3][6] + p[4][7] + p[6][7] + p[7][6] + p[6][3] + p[7][4]) - 22*(p[4][2] + p[2][4] + p[2][6] + p[6][2] + p[4][8] + p[8][4] + p[6][8] + p[8][6]) -24*(p[3][3] + p[3][7] + p[7][3] + p[7][7]) -15*(p[3][2] + p[2][3] + p[2][7] + p[7][2] + p[3][8] + p[8][3] + p[7][8] + p[8][7]) - 8*(p[4][1] + p[1][4] + p[1][6] + p[6][1] + p[4][9] + p[9][4] + p[6][9] + p[9][6]) -7*(p[2][2] + p[2][8] + p[8][8] + p[8][2]) -4*(p[3][1] + p[1][3] + p[7][1] + p[1][7] + p[3][9] + p[9][3] + p[7][9] + p[9][7]) - 1*(p[4][0] + p[0][4] + p[0][6] + p[6][0] + p[4][10] + p[10][4] + p[6][10] + p[10][6]) -2*(p[2][1] + p[1][2] + p[1][8] + p[8][1] + p[2][9] + p[9][2] + p[8][9] + p[9][8]) - 1*(p[0][3] + p[3][0] + p[0][7] + p[7][0] + p[3][10] + p[10][3] + p[7][10] + p[10][7])
		guassian2 = 283*p[5][5] + 160*(p[5][4] + p[5][6] + p[4][5] + p[6][5]) + 15*(p[5][3] + p[5][7] + p[3][5] + p[7][5]) - 17*(p[5][2] + p[2][5] + p[5][8] + p[8][5]) -13*(p[5][1] + p[1][5] + p[5][9] + p[9][5]) - 8*(p[5][0] + p[0][5] + p[5][10] + p[10][5]) + 85*(p[4][4] + p[6][4] + p[4][6] + p[6][6]) -0*(p[4][3] + p[3][4] + p[3][6] + p[4][7] + p[6][7] + p[7][6] + p[6][3] + p[7][4]) - 17*(p[4][2] + p[2][4] + p[2][6] + p[6][2] + p[4][8] + p[8][4] + p[6][8] + p[8][6]) -16*(p[3][3] + p[3][7] + p[7][3] + p[7][7]) -16*(p[3][2] + p[2][3] + p[2][7] + p[7][2] + p[3][8] + p[8][3] + p[7][8] + p[8][7]) - 13*(p[4][1] + p[1][4] + p[1][6] + p[6][1] + p[4][9] + p[9][4] + p[6][9] + p[9][6]) -12*(p[2][2] + p[2][8] + p[8][8] + p[8][2]) -11*(p[3][1] + p[1][3] + p[7][1] + p[1][7] + p[3][9] + p[9][3] + p[7][9] + p[9][7]) - 7*(p[4][0] + p[0][4] + p[0][6] + p[6][0] + p[4][10] + p[10][4] + p[6][10] + p[10][6]) -8*(p[2][1] + p[1][2] + p[1][8] + p[8][1] + p[2][9] + p[9][2] + p[8][9] + p[9][8]) - 6*(p[0][3] + p[3][0] + p[0][7] + p[7][0] + p[3][10] + p[10][3] + p[7][10] + p[10][7]) -4*(p[2][0] + p[0][2] + p[8][0] + p[0][8] + p[2][10] + p[10][2] + p[8][10] + p[10][8]) -5*(p[1][1] + p[9][1] + p[1][9] + p[9][9]) -3*(p[0][1] + p[1][0] + p[9][0] + p[0][9] + p[1][10] + p[10][1] + p[10][9] + p[9][10]) - 1*(p[0][0] + p[10][0] + p[0][10] + p[10][10])
		if guassian > 3000:
			guassianlap.putpixel((i,j),0)
		else:
			guassianlap.putpixel((i,j),1)
		if guassian2 < 10000:
			differencelap.putpixel((i,j),0)
		else:
			differencelap.putpixel((i,j),1)
guassianlap.save('guassianlap.bmp')
differencelap.save('differencelap.bmp')
