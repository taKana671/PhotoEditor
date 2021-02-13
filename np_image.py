from PIL import Image
import numpy as np


def one_color_image(path):
    img = np.array(Image.open(path))

    img_r = img.copy()
    img_r[:, :, (1, 2)] = 0
    img_g = img.copy()
    img_g[:, :, (0, 2)] = 0
    img_b = img.copy()
    img_b[:, :, (0, 1)] = 0
    # img_rgb = np.concatenate((img_r, img_g, img_b), axis=1)
    # img_rgb = np.hstack((img_r, img_g, img_b))
    img_rgb = np.c_['1', img_r, img_g, img_b]
    pil_img = Image.fromarray(img_rgb)
    pil_img.save('numpy_split_color.jpg')


def inverted_negative_image(path):
    img = np.array(Image.open(path).resize((256, 256)))
    # Max値から画素値を引く
    img_i = 255 - img 
    Image.fromarray(img_i).save('numpy_inverse.jpg')


def reduce_color(path):
    img = np.array(Image.open(path).resize((256, 256)))
    img_32 = img // 32 * 32
    img_128 = img // 128 * 128
    img_dec = np.concatenate((img, img_32, img_128), axis=1)
    Image.fromarray(img_dec).save('dec_color_png.jpg')


def binarization(path):
    thresh = 128
    maxval = 255
    im_gray = np.array(Image.open(path).convert('L'))
    im_bin = (im_gray > thresh) * maxval
    Image.fromarray(np.uint8(im_bin)).save('numpy_binarization.png')


def binarization_keep(path):
    thresh = 128
    im_gray = np.array(Image.open(path).convert('L'))
    im_bin = (im_gray > thresh) * im_gray
    Image.fromarray(np.uint8(im_bin)).save('numpy_binarization_keep.png')


def image_binarization(path):
    thresh = 128
    im_gray = np.array(Image.open(path).convert('L'))
    im_bool = im_gray > thresh
    im_dst = np.empty((*im_gray.shape, 3))
    r, g, b = 255, 128, 32
    im_dst[:, :, 0] = im_bool * r
    im_dst[:, :, 1] = im_bool * g
    im_dst[:, :, 2] = im_bool * b
    Image.fromarray(np.uint8(im_dst)).save('binarization_color.png')

    im_dst[:, :, 0] = im_bool * r
    im_dst[:, :, 1] = ~im_bool * g
    im_dst[:, :, 2] = im_bool * b
    Image.fromarray(np.uint8(im_dst)).save('binarization_color2.png')


def image_binarization2(path):
    img = np.array(Image.open(path))
    img_th = np.empty_like(img)
    thresh = 128
    maxval = 255

    for i in range(3):
        img_th[:, :, i] = (img[:, :, i] > thresh) * maxval
    Image.fromarray(np.uint8(img_th)).save('binarization_color3.png')

    l_thresh = [64, 128, 192]
    l_maxval = [64, 128, 192]
    for i, thresh, maxval in zip(range(3), l_thresh, l_maxval):
        img_th[:, :, i] = (img[:, :, i] > thresh) * maxval
    Image.fromarray(np.uint8(img_th)).save('binarization_color4.png')
    



if __name__ == '__main__':
    image_binarization('19615_en_1.jpg')
    # reduce_color('lena2.png')
    # inverted_negative_image('lena.jpg')
    # one_color_image('lena.jpg')
