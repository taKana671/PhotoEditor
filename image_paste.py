from PIL import Image, ImageDraw, ImageFilter, ImageOps


def paste_image(img1, img2):
    # 位置指定なしだと左上に貼り付けられる
    # pasteメソッドではベース自体が上書きされるため
    # 元の画像を残したい場合はcopy()してから使う
    back = img1.copy()
    back.paste(img2)
    # back.show()
    # back.save('pasted.jpg', quality=95)
    back.save('pasted.jpg', quality=95)


def paste_image_position(img1, img2, x, y):
    back = img1.copy()
    # 貼り付ける位置は、pasteメソッドの第二引数boxに
    # タプル（左上のx座標、左上のy座標）で指定。
    # 貼り付け画像がベース画像の領域外にはみ出す場合、はみ出した部分は無視される。
    back.paste(img2, (x, y))
    back.save('pasted.jpg')


def use_mask(img1, img2):
    mask = Image.new("L", img2.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((500, 300, 800, 600), fill=255)
    mask_blur = mask.filter(ImageFilter.GaussianBlur(10))
    # mask_blur.show()
    back = img1.copy()
    # back.paste(img2, (0, 0), mask)
    back.paste(img2, (0, 0), mask_blur)
    back.save('mask_circle.jpg')


def use_mask2(img1, img2):
    # マスクに使う写真がpngだと、convert('RGB') にしてもうまくいかない
    heart = Image.open('black_heart.jpeg').resize(img2.size).convert('L')
    # heart.show()
    black_heart = ImageOps.invert(heart)
    # black_heart.show()
    back = img1.copy()
    back.paste(img2, (300, 300), black_heart)
    back.save('heart_flower.jpg')


def composite(img1, img2):
    mask = Image.new('L', img1.size, 128)
    img = Image.composite(img1, img2, mask)
    # img = Image.blend(img1, img2, 0.5)
    img.save('composite2.jpg')




if __name__ == '__main__':
    path1 = '18980_en_1.jpg'
    # path2 = 'center.jpg'
    # path2 = '19883_en_1.jpg'
    path2 = '19694_en_1.jpg'
    
    img1 = Image.open(path1)
    img2 = Image.open(path2)
    # composite(img1, img2)

    mask = Image.open('gray_gradient_v.jpg').convert('L').resize(img1.size)
    new = Image.composite(img1, img2, mask)
    new.save('comosite4.jpg')

    # use_mask2(img1, img2)
    # paste_image_position(img1, img2, 150, 100)
    # paste_image(img1, img2)
