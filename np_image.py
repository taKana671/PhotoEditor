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

if __name__ == '__main__':
    reduce_color('lena2.png')
    # inverted_negative_image('lena.jpg')
    # one_color_image('lena.jpg')
