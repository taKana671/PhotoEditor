from PIL import Image, ImageDraw, ImageFilter


def paste_image(img1, img2):
    # 位置指定なしだと左上に貼り付けられる
    # pasteメソッドではベース自体が上書きされるため
    # 元の画像を残したい場合はcopy()してから使う
    back = img1.copy()
    back.paste(img2)
    # back.show()
    back.save('pasted.jpg')


if __name__ == '__main__':
    path1 = '18980_en_1.jpg'
    path2 = 'center.jpg'
    img1 = Image.open(path1)
    img2 = Image.open(path2)
    
    paste_image(img1, img2)
