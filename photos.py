from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps


def get_image_data(path):
    img = Image.open(path)
    print(img.format, img.size, img.mode)
    img.show()

    
def resize_image(path):
    img = Image.open(path)
    # new_img = img.resize((300, 200))
    # new_img.show()

    # 以下は縦横比を維持したままリサイズする。破壊的メソッド
    new_img = img.copy()
    new_img.thumbnail((300, 200))
    new_img.save('resized_img.jpg')


def rotate_image(path, angle):
    img = Image.open(path)
    new_img = img.rotate(angle)
    new_img.save('rotate.jpg')
    im_rotate = img.rotate(45, fillcolor=(255, 128, 0), expand=True)
    im_rotate.save('rotate2.jpg')

def transpose_image(path):
    img = Image.open(path)
    new_image = img.transpose(Image.FLIP_LEFT_RIGHT)
    new_image.save('left_right.jpg')
    new_image = img.transpose(Image.FLIP_TOP_BOTTOM)
    new_image.save('top_bottom.jpg')


# coordinates: 左上と右下のX座標とY座標のタプル
# (左上x, 左上y, 右下x, 右下y )
def trim_image(path, coordinates):
    img = Image.open(path)
    new_img = img.crop(coordinates)
    new_img.save('trimed.jpg')    


def crop_center(img, crop_width, crop_height):
    # 画像の中心を切り出す
    # img = Image.open(path)
    img_width, img_height = img.size
    new_img = img.crop((
        (img_width - crop_width) // 2,
        (img_height - crop_height) // 2,
        (img_width + crop_width) // 2,
        (img_height + crop_height) // 2
    )) 
    return new_img


def crop_max_square(img):
    return crop_center(img, min(img.size), min(img.size))


def mask_circle_solid(img, background_color, blur_radius, offset=0):
    background = Image.new(img.mode, img.size, background_color)
    offset = blur_radius * 2 + offset
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, img.size[0] - offset, img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    return Image.composite(img, background, mask)


def mask_circle_transparent(img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, img.size[0] - offset, img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    result = img.copy()
    result.putalpha(mask)
    return result


# def crop_max_square(path):
#     # 長方形から最大サイズの正方形を切り出す
#     img = Image.open(path)
#     crop_center(path, min(img.size), min(img.size))


def grey_scale(path):
    img = Image.open(path)
    new_img = img.convert('L')
    new_img.save('grey_scale.jpg')


def contrast(path):
    img = Image.open(path)
    # point: 画像のピクセル値を一括して変換
    # 今回は1.5倍に変換
    new_img = img.point(lambda x: x * 1.5)
    new_img.save('contrast.jpg')


def mosaic_over(path):
    # mosaic専用のメソッドはないが、
    # 本来の画像よりサイズを小さくすると差分の色情報が失われ、
    # 画像が劣化する。これを利用すると、モザイクっぽくなる。
    img = Image.open(path)
    # 64 x 64に縮小してから元のサイズにもどす
    new_img = img.resize((64, 64)).resize((512, 512))
    new_img.save('mosaic.jpg')


def gause(path):
    # ぼかし処理はImageオブジェクトのfilterメソッドを使います。
    # 引数にはImageFilterオブジェクトのGaussianBlurを指定。
    # ぼかしの強度も指定できます。
    img = Image.open(path)
    new_img = img.filter(ImageFilter.GaussianBlur(4))
    new_img.save('gause.jpg')


def write_text(path):
    img = Image.open(path)
    new_img = img.copy()
    draw = ImageDraw.Draw(new_img)
    font = ImageFont.truetype('arial.ttf', 32)
    draw.text((0, 0), 'Hello, girls!', font=font)
    new_img.save('draw_text.jpg')


def drawing(path):
    img = Image.open(path)
    new_img = img.copy()
    draw = ImageDraw.Draw(new_img)
    # 線の描画:線の開始点と終了点を示すX座標とY座標、
    # 線の色、線の幅などを指定
    xy = [(0, 0), (512, 0), (0, 512), (512, 512)]
    draw.line(xy, fill=(0, 0, 255), width=10)
    new_img.save('draw_line.jpg')
    # 長方形はrectangleメソッドに左上と右下の座標を指定する
    # fillで長方形の色、outlineで線の色、widthで線の幅。
    new_img = img.copy()
    draw = ImageDraw.Draw(new_img)
    draw.rectangle(
        [(0, 0), (256, 256)],
        fill=(0, 0, 255),
        outline=(0, 255, 0),
        width=10
    )
    new_img.save('draw_rectangle.jpg')
    # 楕円はellipseメソッドを使い,
    # 長方形同様、楕円の色や線の色、線の幅を指定できる。
    new_img = img.copy()
    draw = ImageDraw.Draw(new_img)
    draw.ellipse(
        [(0, 0), (256, 256)],
        fill=(0, 0, 255),
        outline=(0, 255, 0),
        width=10
    )
    new_img.save('draw_orval.jpg')


def invert_img(path):
    # 各画素の値を最大値（8ビットの場合は255）から引いた値に置き換えているだけ。
    # 例えば、0は255、64は191、255は0となる
    img = Image.open(path)
    img_invert = ImageOps.invert(img)
    img_invert.save('invert.jpg')


def invert_png(path):
    # 透過pngをopen()で読み込むとmodeがRGBAとなり正しく処理されないので、
    # convert()でRGBに変換する。
    img = Image.open(path).convert('RGB')
    img_invert = ImageOps.invert(img)
    img_invert.save('invert_png.png')


def flip_mirror(path):
    img = Image.open(path)
    img_flip = ImageOps.flip(img)
    img_flip.save('flip.jpg')
    img_mirror = ImageOps.mirror(img)
    img_mirror.save('mirror.jpg')



if __name__ == '__main__':
    path = 'lena.jpg'
    # path1 = '2883.png'
    path2 = '19883_en_1.jpg'

    img = Image.open('astronaut_rect.bmp')
    img_square = crop_max_square(img).resize((200, 200), Image.LANCZOS)
    img_thumb = mask_circle_transparent(img_square, 4)
    # 透過画像はpngで保存する
    img_thumb.save('mask_circle_transparent.png')

    # img = Image.open('astronaut_rect.bmp')
    # img_square = crop_max_square(img).resize((200, 200), Image.LANCZOS)
    # img_thumb = mask_circle_solid(img_square, (0, 0, 0), 4)
    # img_thumb.save('mask_circle_solid.jpg')

    # flip_mirror('heart_flower.jpg')  
    # invert_png('2883.png')
    # crop_max_square(path2)
    # crop_center(path2, 300, 300)
    # drawing(path)
    # write_text(path)
    # gause(path)
    # mosaic_over(path)
    # contrast(path)
    # grey_scale(path)
    # trim_image(path, (170, 170, 400, 400))
    # transpose_image(path)
    rotate_image(path2, 45)
    # resize_image(path)
    # get_image_data(path1)