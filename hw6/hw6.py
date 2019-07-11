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
for i in range(512):
	for j in range(512):
		if img.getpixel((i,j)) < 128:
			img2.putpixel((i, j), 0)
		elif img.getpixel((i,j)) >= 128:
			img2.putpixel((i, j), 1)
img3 = Image.new("1", (64, 64))
for i in range(64):
	for j in range(64):
		img3.putpixel((i, j), img2.getpixel((i*8, j*8)))
f = open("yokoi.txt", "w")

for j in range(64):
	for i in range(64):
		if img3.getpixel((i,j)) == 1:
			label = [0 for i in range(8)]
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
			if countr == 4:
				f.write('5')
			elif countq != 0:
				f.write(str(countq))
			else :
				f.write(' ')
		else:
			f.write(' ')
	f.write('\n')


