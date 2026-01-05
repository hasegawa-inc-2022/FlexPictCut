import PyInstaller.__main__
import tkinterdnd2
import os

# tkinterdnd2のパスを取得
dnd_path = os.path.dirname(tkinterdnd2.__file__)

PyInstaller.__main__.run([
    'main.py',              # あなたのプログラムのファイル名
    '--onefile',            # 1つのEXEにまとめる
    '--noconsole',          # 実行時に黒い画面（コンソール）を出さない
    '--icon=public/icon/app_ico.ico',
    f'--add-data={dnd_path}{os.pathsep}tkinterdnd2', # D&D用ライブラリを含める
    '--clean',
    '--name=FlexPictCutter',    # 出力されるEXEの名前
])