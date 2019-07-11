from PIL import Image, ImageFile, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

class row_class():
	"""docstring for row_class"""
	def __init__(self, row, startc, endc, perm_label, count):
		self.row = row
		self.startc = startc
		self.endc = endc
		self.perm_label = perm_label
		self.count = count

class labelset():
	"""docstring for """
	def __init__(self, label, nextt, left, right, up, down, area):
		self.label = label
		self.next = nextt
		self.left = left
		self.right = right
		self.up = up
		self.down = down
		self.area = area
		
class rectangle():
	def __init__(self, left, right, up, down, area):
		self.left = left
		self.right = right
		self.up = up
		self.down = down
		self.area = area

img=(Image.open("lena.bmp")).convert("L")
w, h = img.size
pixel = [[None]*347 for i in range(348)]
img2 = Image.new("1", (w, h))
x = np.arange(256)
histogram = [0 for i in range(256)]
for i in range(w):
	for j in range(h):
		histogram[img.getpixel((i,j))] += 1
		if img.getpixel((i,j)) < 128:
			img2.putpixel((i, j), 0)
		elif img.getpixel((i,j)) >= 128:
			img2.putpixel((i, j), 1)
img2.save("lena2.bmp")
plt.bar(x,histogram,facecolor = 'black',edgecolor = 'black')
plt.xlim(0,255)
plt.xticks(np.linspace(0,255,2))
plt.title('lena histogram')
plt.savefig('histogram.jpg')
state = 0
rowclass = []
rowrecord = []
classcount = 0
for i in range(w):
	rowrecord.append(classcount)
	state = 0
	for j in range(h):
		if img2.getpixel((i,j)) == 0:
			if state == 0:
				state = 1
				rowclass.append(row_class(i,j,j,0,1))
				classcount += 1
			elif state == 1:
				rowclass[classcount - 1].endc = j
				rowclass[classcount - 1].count += 1
		if img2.getpixel((i, j)) == 1:
			state = 0
rowrecord.append(classcount)

labelnum = 0
label = []
for i in range(rowrecord[0],rowrecord[1]):
	labelnum += 1
	rowclass[i].perm_label = labelnum
	label.append(labelset(labelnum, 0, rowclass[i].startc, rowclass[i].endc, rowclass[i].row, rowclass[i].row, rowclass[i].perm_label))
for row in range(1,511):
	i = rowrecord[row - 1]
	j = rowrecord[row]
	while i < rowrecord[row] and j < rowrecord[row+1]:
		if rowclass[i].startc > rowclass[j].endc:
			if rowclass[j].perm_label == 0:
				labelnum += 1
				rowclass[j].perm_label = labelnum
				label.append(labelset(labelnum, 0, rowclass[j].startc, rowclass[j].endc, row, row, rowclass[j].count))
			j += 1
		elif rowclass[i].endc < rowclass[j].startc:
			i += 1
		else:
			if rowclass[j].perm_label == 0:
				rowclass[j].perm_label = rowclass[i].perm_label
				label[rowclass[i].perm_label - 1].area += rowclass[j].count
			else:
				x = label[rowclass[i].perm_label - 1]
				y = label[rowclass[j].perm_label - 1]
				numx = rowclass[i].perm_label
				numy = rowclass[i].perm_label
				while x.label != numx + 1:
					numx = x.label - 1
					x = label[numx]
				while y.label != numy + 1:
					numy = y.label - 1
					y = label[numy]
				if numx > numy:
					label[rowclass[i].perm_label - 1].label = numy + 1
				else:
					label[rowclass[j].perm_label - 1].label = numx + 1
			#劃框框
			label[rowclass[j].perm_label - 1].down = row
			if rowclass[j].startc < label[rowclass[j].perm_label - 1].left:
				label[rowclass[j].perm_label - 1].left = rowclass[j].startc
			if rowclass[j].endc > label[rowclass[j].perm_label - 1].right:
				label[rowclass[j].perm_label - 1].right = rowclass[j].endc
			#判斷下一個是誰
			if rowclass[i].endc < rowclass[j].endc:
				i += 1
			elif rowclass[i].endc > rowclass[j].endc:
				j += 1
			elif rowclass[i].endc == rowclass[j].endc:
				i += 1
				j += 1
	while j < rowrecord[row+1] :
		if rowclass[j].perm_label == 0:
			labelnum += 1
			rowclass[j].perm_label = labelnum
			label.append(labelset(labelnum, 0, rowclass[j].startc, rowclass[j].endc, row, row, rowclass[j].count))
		j += 1
answer = []
for i in range(labelnum):
	answer.append(rectangle(512,0,512,0,0))
for i in range(labelnum):
	x = label[i]
	num = i
	while x.label != num + 1:
		num = x.label - 1
		x = label[num]
	answer[x.label - 1].area += label[i].area
	if label[i].left < answer[x.label - 1].left:
		answer[x.label - 1].left = label[i].left
	if label[i].right > answer[x.label - 1].right:
		answer[x.label - 1].right = label[i].right
	if label[i].up < answer[x.label - 1].up:
		answer[x.label - 1].up = label[i].up
	if label[i].down > answer[x.label - 1].down:
		answer[x.label - 1].down = label[i].down
img3 = img2.convert('P')
draw = ImageDraw.Draw(img3)
#draw.line(((420,0), (420,511)),128)
for i in range(labelnum):
	if answer[i].area > 500:
		draw.rectangle((answer[i].up,answer[i].left,answer[i].down,answer[i].right),outline = 128)
img3.save("lena3.bmp")





