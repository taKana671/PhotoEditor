import numpy as np
from PIL import Image


def get_gradient_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T



def get_gradient_3d(width, height, start_list, stop_list, is_horizontal_list):
    result = np.zeros((height, width, len(start_list)), dtype=np.float)

    for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)
    return result



if __name__ == '__main__':
    # array = get_gradient_3d(512, 256, (0, 0, 192), (255, 255, 64), (True, False, False))
    # Image.fromarray(np.uint8(array)).save('gray_gradient_v.jpg', quality=95)

    array = get_gradient_3d(1920, 1200, (0, 0, 0), (255, 255, 255), (False, False, False))
    Image.fromarray(np.uint8(array)).save('gray_gradient_v.jpg', quality=95)

    # array = get_gradient_3d(1920, 1200, (0, 0, 0), (255, 255, 255), (True, True, True))
    # Image.fromarray(np.uint8(array)).save('gray_gradient.jpg', quality=95)


