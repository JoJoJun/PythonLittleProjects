'''
将图片转字符
思想是将字符看作大的像素，一种字符代表一种颜色
'''
from PIL import Image
import argparse

# parameters
#python命令行解析工具 ： argparse
parser = argparse.ArgumentParser()#创建解析对象
parser.add_argument('file')#每个add对应一个关注的参数或选项
parser.add_argument('-o','--output')
parser.add_argument('--width',type = int,default = 80)
parser.add_argument('--height',type=int,default = 80)
#get parameters
args = parser.parse_args()#解析参数
IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output
#字符
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
#转换函数
def get_char(r,g,b,alpha=256):
	if alpha == 0:
		return ' '
	length = len(ascii_char)
    #灰度公式
	gray = int(0.2126*r+0.7152*g+0.0722*b)
	unit = (256.0+1)/length
	return ascii_char[int(gray/unit)] #将色素映射到每个字符

if  __name__ == '__main__':
	im = Image.open(IMG)
	im = im.resize((WIDTH,HEIGHT),Image.NEAREST)

	txt = ""
	for i in range(HEIGHT):
		for j in range(WIDTH):
			txt += get_char(*im.getpixel((j,i)))#返回指定位置的像素
		txt += '\n'
	print(txt)

	if OUTPUT:
		with open(OUTPUT,'w') as f:
			f.write(txt)
	else:
		with open("output.txt",'w') as f:
			f.write(txt)