# from PIL import Image

# # 切り抜いた正方形の画像を開く
# img = Image.open("./public/png/Gemini_Generated_Image_xc14n4xc14n4xc14_crop.png")

# # Windowsアイコン用の標準サイズセット
# icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

# # ICOファイルとして保存
# img.save("app_icon.ico", sizes=icon_sizes)
# print("app_icon.ico が作成されました")

from PIL import Image

# 1. 元の高品質PNGを読み込む
img = Image.open("./public/png/Gemini_Generated_Image_xc14n4xc14n4xc14_crop.png")

# 2. Windowsアイコン用のサイズリスト
icon_sizes = [16, 32, 48, 64, 128, 256]
images = []

for size in icon_sizes:
    # 各サイズに合わせて高品質リサイズを実行
    temp_img = img.resize((size, size), Image.LANCZOS)
    images.append(temp_img)

# 3. 最初の画像（256x256など）をベースに、他のサイズを同梱して保存
# append_imagesにリサイズ済みのリストを渡します
images[-1].save(
    "app_ico.ico", 
    format="ICO", 
    append_images=images[:-1]
)

print("高品質な app_ico.ico が作成されました")