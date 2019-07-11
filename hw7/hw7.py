from PIL import Image, ImageFile, ImageDraw

def h(b,c,d,e,countq,countr):
	if b == c and b == d and b == e:
		return (countq, countr + 1)
	elif b != c:
		return (countq, countr)
	else :
		return (countq + 1, countr)

img=(Image.open("lena.bmp")).convert("L")
img2 = Image.new("1", (512, 512))
neighbor = [(1,0),(0,-1),(-1,0),(0,1),(1,1),(1,-1),(-1,-1),(-1,1)]
fourconnect = [(1,0), (0,1), (-1,0), (0,-1)]

for i in range(512):
	for j in range(512):
		if img.getpixel((i,j)) < 128:
			img2.putpixel((i, j), 0)
		elif img.getpixel((i,j)) >= 128:
			img2.putpixel((i, j), 1)
img3 = Image.new("1", (64, 64))
for i in range(64):
	for j in range(64):
		pix = img2.getpixel((i*8, j*8))
		img3.putpixel((i, j), pix)
while True:
	borderimg = [[0]*64 for i in range(64)]
	markedimg = [[0]*64 for i in range(64)]
	for j in range(64):
		for i in range(64):
			if img3.getpixel((i,j)) == 1:
				label = [0 for k in range(8)]
				countq = 0
				countr = 0
				for k in range(8):
					x = i + neighbor[k][0]
					y = j + neighbor[k][1]
					if 0 <= x < 64 and 0 <= y < 64:
						label[k] = img3.getpixel((x,y))
					else:
						label[k] = 0
				(countq, countr) = h(1, label[0], label[1], label[5], countq, countr)
				(countq, countr) = h(1, label[1], label[2], label[6], countq, countr)
				(countq, countr) = h(1, label[2], label[3], label[7], countq, countr)
				(countq, countr) = h(1, label[3], label[0], label[4], countq, countr)
				if countq != 0:
					borderimg[i][j] = countq
				if countr == 4:
					borderimg[i][j] = 5
	for j in range(64):
		for i in range(64):
			if borderimg[i][j] != 0:
				num = 0
				for k in range(4):
					x = i + fourconnect[k][0]
					y = j + fourconnect[k][1]
					if 0 <= x < 64 and 0 <= y < 64:
						if borderimg[x][y] == 1:
							num += 1
				if num == 0 or borderimg[i][j] != 1:
					markedimg[i][j] = 'q'
				elif num > 0 and borderimg[i][j] == 1 :
					markedimg[i][j] = 'p'
				
	change = 0
	for j in range(64):
		for i in range(64):
			if markedimg[i][j] == 'p':
				label = [0 for k in range(8)]
				countq = 0
				countr = 0
				for k in range(8):
					x = i + neighbor[k][0]
					y = j + neighbor[k][1]
					if 0 <= x < 64 and 0 <= y < 64:
						label[k] = img3.getpixel((x,y))
					else:
						label[k] = 0
				(countq, countr) = h(1, label[0], label[1], label[5], countq, countr)
				(countq, countr) = h(1, label[1], label[2], label[6], countq, countr)
				(countq, countr) = h(1, label[2], label[3], label[7], countq, countr)
				(countq, countr) = h(1, label[3], label[0], label[4], countq, countr)
				if countq == 1 and markedimg[i][j] == 'p':
					img3.putpixel((i,j), 0)
					change += 1
	print(change)
	if change == 0:
		break

img3.save("thinning.bmp")
				


