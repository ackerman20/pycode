from PIL import Image, ImageDraw, ImageFont

img  = Image.open("D:/Introdunction_to_Digital_Communication/2_1.jpg")
Myfont  = ImageFont.truetype('D://PY_code/wt014.ttf', size=100)

#Initialization & Use Srcimg as background
Drawimg = ImageDraw.Draw(img)

w,h = img.size
print(img.size)
x = img.width*(1/4)
y = img.height/2
text = Image.new(mode='RGBA', size=(600, 150), color=(255, 0, 0, 0))
draw = ImageDraw.Draw(text)
#Draw text on image
Drawimg.text((x, y), 'Your馬的', fill=(0, 0, 0), font=Myfont)
text = text.rotate(10,expand=1)

img.show(img)
#img.save('D:/Introdunction_to_Digital_Communication/HelloWorld.jpg')