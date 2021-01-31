from PIL import Image, ImageDraw

images = []

width, height = 200, 200
center = width // 2
color1 = (0, 0, 0)
color2 = (255, 255, 255)
max_radius = int(center * 1.5)
step = 8

for i in range(0, max_radius, step):
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    draw.ellipse((center - i, center - i, center + i, center + i), fill=color2)
    images.append(img)

for i in range(0, max_radius, step):
    img = Image.new('RGB', (width, height), color2)
    draw = ImageDraw.Draw(img)
    draw.ellipse((center - i, center - i, center + i, center + i), fill=color1)
    images.append(img)

print(len(images))
images[0].save('imagedraw.gif', save_all=True, append_images=images[1:],
    optimize=False, duration=40, loop=0)