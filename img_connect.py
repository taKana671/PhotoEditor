from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps


def concat_h(img1, img2):
    dst = Image.new('RGB', (img1.width + img2.width, img1.height))
    dst.paste(img1, (0, 0))
    dst.paste(img2, (img1.width, 0))
    return dst


def concat_v(img1, img2):
    dst = Image.new('RGB', (img.width, img2.height + img2.height))
    dst.paste(img1, (0, 0))
    dst.paste(img2, (0, img1.height))
    return dst


def concat_h_cut(img1, img2):
    # PillowのImage.paste()では
    # 貼り付け先の画像の範囲外にはみ出した部分は無視される（カットされる）
    dst = Image.new('RGB', (img1.width + img2.width, min(img1.height, img2.height)))
    dst.paste(img1, (0, 0))
    dst.paste(img2, (img1.width, 0))
    return dst


def concat_v_cut(img1, img2):
    dst = Image.new('RGB', (min(img1.width, img2.width), img1.height + img2.height))
    dst.paste(img1, (0, 0))
    dst.paste(img2, (0, img1.height))
    return dst


def concat_h_cut_center(img1, img2):
    larger = max(img1, img2, key=lambda x: x.height)
    smaller = min(img1, img2, key=lambda x: x.height)
    dst = Image.new('RGB', (larger.width + smaller.width, smaller.height))
    dst.paste(smaller, (0, 0))
    dst.paste(larger, (smaller.width, (smaller.height - larger.height) // 2))
    return dst


def concat_v_cut_center(img1, img2):
    larger = max(img1, img2, key=lambda x: x.width)
    smaller = min(img1, img2, key=lambda x: x.width)
    dst = Image.new('RGB', (smaller.width, smaller.height + larger.height))
    dst.paste(smaller, (0, 0))
    dst.paste(larger, ((smaller.width - larger.width) // 2, smaller.height))
    return dst


def concat_h_blank(img1, img2, color=(0, 0, 0)):
    dst = Image.new('RGB', (img1.width + img2.width, max(img1.height, img2.height)), color)
    dst.paste(img1, (0, 0))
    dst.paste(img2, (img1.width, 0))
    return dst


def concat_v_blank(img1, img2, color=(0, 0, 0)):
    dst = Image.new('RGB', (max(img1.width, img2.width), img1.height + img2.height), color)
    dst.paste(img1, (0, 0))
    dst.paste(img2, (0, img1.height))
    return dst


def concat_h_resize(img1, img2, resample=Image.BICUBIC, resize_big_image=True):
    # 拡大すると画質が低下するので、基本的には大きい画像を小さくリサイズ（縮小）したほうがいい
    if img1.height == img2.height:
        _img1, _img2 = img1, img2
    elif ((img1.height > img2.height and resize_big_image) or 
            (img1.height < img2.height and not resize_big_image)):
        _img1 = img1.resize((int(img1.width * img2.height / img1.height), img2.height), resample=resample)
        _img2 = img2
    else:
        _img1 = img1
        _img2 = img2.resize((int(img2.width * img1.height / img2.height), img1.height), resample=resample)
    dst = Image.new('RGB', (_img1.width + _img2.width,  + _img1.height))
    dst.paste(_img1, (0, 0))
    dst.paste(_img2, (_img1.width, 0))
    return dst


def concat_v_resize(img1, img2, resample=Image.BICUBIC, resize_big_image=True):
    if img1.width == img2.width:
        _img1, _img2 = img1, img2
    elif ((img1.width > img2.width and resize_big_image) or 
            (img1.width < img2.width and not resize_big_image)):
        _img1 = img1.resize((img2.width, int(img1.height * img2.width / img1.width)), resample=resample)
        _img2 = img2
    else:
        _img1 = img1
        _img2 = img2.resize((img1.width, int(img2.height * img1.width / img2.width)), resample=resample)
    dst = Image.new('RGB', (_img1.width,  _img2.height + _img1.height))
    dst.paste(_img1, (0, 0))
    dst.paste(_img2, (0, _img1.height))
    return dst


def concat_h_multi_blank(img_list):
    _img = img_list[0]
    for img in img_list[1:]:
        _img = concat_h_blank(_img, img)
    return _img


def concat_h_multi_resize(img_list, resample=Image.BICUBIC):
    min_height = min(img.height for img in img_list)
    imgs_resized = [img.resize((int(img.width * min_height / img.height), min_height), resample=resample)
        for img in img_list]
    total_width = sum(img.width for img in imgs_resized)
    dst = Image.new('RGB', (total_width, min_height))
    pos_x = 0
    for img in imgs_resized:
        dst.paste(img, (pos_x, 0))
        pos_x += img.width
    return dst


def concat_v_multi_resize(img_list, resample=Image.BICUBIC):
    min_width = min(img.width for img in img_list)
    imgs_resized = [img.resize((min_width, int(img.height * min_width / img.width)), resample=resample)
        for img in img_list]
    total_height = sum(img.height for img in imgs_resized)
    dst = Image.new('RGB', (min_width, total_height))
    pos_y = 0
    for img in imgs_resized:
        dst.paste(img, (0, pos_y))
        pos_y += img.height
    return dst


def concat_tile_resize(imgs_list, resample=Image.BICUBIC):
    imgs_v = [concat_h_multi_resize(sub_list, resample=resample) for sub_list in imgs_list]
    return concat_v_multi_resize(imgs_v, resample=resample)


def concat_h_repeat(img, column):
    dst = Image.new('RGB', (img.width * column, img.height))
    for x in range(column):
        dst.paste(img, (x * img.width, 0))
    return dst

def concat_v_repeat(img, row):
    dst = Image.new('RGB', (img.width, img.height * row))
    for y in range(row):
        dst.paste(img, (0, y * img.height))
    return dst


def concat_tile_repeat(img, row, column):
    dst_h = concat_h_repeat(img, column)
    return concat_v_repeat(dst_h, row)


if __name__ == '__main__':
    path1 = 'lena.jpg'
    path2 = 'rocket.jpg'
    path3 = '19883_en_1.jpg'
    path4 = '2883.png'
    # img1 = Image.open(path1)
    # img2 = Image.open(path2)

    concat_tile_repeat(Image.open(path4), 3, 4).save('tile_heart.jpg')

    # concat_tile_resize([[img1], [img1, img2], [img1, img2, img1]]).save('tile_resize.jpg')

    # concat_h_multi_resize([img1, img2, img1]).save('resize_multih.jpg')
    # concat_v_multi_resize([img1, img2, img1]).save('resize_multiv.jpg')
    # concat_v_resize(img2, img1).save('concat_v_resize.jpg')
    # concat_v_blank(img1, img2).save('concat_v_blank.jpg')