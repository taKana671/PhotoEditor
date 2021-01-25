from PIL import Image

def put_alpha(alpha, img):
    # 0は100%透過、 255は0%透過（不透過）
    # 128だと128/255でおよそ50%
    img_rgba = img.copy()
    img_rgba.putalpha(alpha)
    # png画像を作るメソッドのため、pngを指定
    img_rgba.save('put_alpha.png')


if __name__ == '__main__':
    path = '19883_en_1.jpg'
    img = Image.open(path)
    put_alpha(0, img)