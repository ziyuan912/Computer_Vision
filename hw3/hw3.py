from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = (Image.open("lena.bmp")).convert("L")
w, h = img.size
img2 = Image.new("L", (w,h))
img3 = Image.new("L", (w,h))
histogram = [0 for i in range(256)]
histogram2 = [0 for i in range(256)]
xx = np.arange(256)
xxx = np.arange(256)
new = [0 for i in range(256)]
sums = 0
for i in range(w):
	for j in range(h):
		x = int(img.getpixel((i,j))/3)
		histogram[x] += 1
		img2.putpixel((i, j), x)
		sums += 1
now = 0
for i in range(256):
	now += histogram[i]
	#print(histogram[i])
	new[i] = int(255*now/sums)
for i in range(w):
	for j in range(h):
		img3.putpixel((i,j), new[img2.getpixel((i,j))])
		histogram2[new[img2.getpixel((i,j))]] += 1
for i in range(256):
	print(histogram2[i])
img3.save("lena3.bmp")
img2.save("lena2.bmp")
plt.bar(xx,histogram,facecolor = 'black',edgecolor = 'black')
plt.xlim(0,255)
plt.xticks(np.linspace(0,255,2))
plt.title('without histogram equalization')
plt.savefig('histogram_1.jpg')
plt.bar(xxx,histogram2,facecolor = 'black',edgecolor = 'black')
plt.xlim(0,255)
plt.xticks(np.linspace(0,255,2))
plt.title('histogram equalization')
plt.savefig('histogram_2.jpg')