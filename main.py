import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD

class ScaledPictCutterV4:
    def __init__(self, root):
        self.root = root
        self.root.title("FlexPictCutter")
        self.root.geometry("800x600")

        # 変数の初期化
        self.src_img = None
        self.display_img = None
        self.scale = 1.0
        self.rect = None
        self.current_file_path = ""
        self.rect_w = 300
        self.rect_h = 200
        self.start_x = 0
        self.start_y = 0

        # --- 操作パネル ---
        self.controls = tk.Frame(root)
        self.controls.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Label(self.controls, text="横幅(px):").pack(side=tk.LEFT)
        self.ent_w = tk.Entry(self.controls, width=6)
        self.ent_w.insert(0, str(self.rect_w))
        self.ent_w.pack(side=tk.LEFT, padx=5)
        # Enterキーを枠更新メソッドにバインド
        self.ent_w.bind("<Return>", lambda e: self.update_rect_size())

        tk.Label(self.controls, text="縦幅(px):").pack(side=tk.LEFT)
        self.ent_h = tk.Entry(self.controls, width=6)
        self.ent_h.insert(0, str(self.rect_h))
        self.ent_h.pack(side=tk.LEFT, padx=5)
        # Enterキーを枠更新メソッドにバインド
        self.ent_h.bind("<Return>", lambda e: self.update_rect_size())

        self.btn_update = tk.Button(self.controls, text="枠を更新", command=self.update_rect_size)
        self.btn_update.pack(side=tk.LEFT, padx=10)

        self.btn_save = tk.Button(self.controls, text="選択範囲を保存", bg="skyblue", command=self.save_crop)
        self.btn_save.pack(side=tk.RIGHT, padx=10)

        # --- キャンバス ---
        self.canvas = tk.Canvas(root, cursor="fleur", bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', lambda e: self.load_image(e.data.strip('{}')))

        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.move_rect)
        self.root.bind("<Configure>", self.on_window_resize)

    def update_rect_size(self):
        """入力された数値で枠のサイズを更新する"""
        try:
            val_w = int(self.ent_w.get())
            val_h = int(self.ent_h.get())
            
            # 画像が読み込まれている場合は画像サイズで制限
            if self.src_img:
                self.rect_w = min(val_w, self.src_img.width)
                self.rect_h = min(val_h, self.src_img.height)
            else:
                self.rect_w = val_w
                self.rect_h = val_h
            
            # 入力値を整形して再表示
            self.ent_w.delete(0, tk.END); self.ent_w.insert(0, str(self.rect_w))
            self.ent_h.delete(0, tk.END); self.ent_h.insert(0, str(self.rect_h))

            if self.rect:
                coords = self.canvas.coords(self.rect)
                self.limit_and_move(coords[0], coords[1])
        except ValueError:
            messagebox.showerror("エラー", "数値（半角数字）を入力してください")

    # --- 以下、画像処理・移動・保存ロジック（前バージョンと同じ） ---

    def load_image(self, file_path):
        try:
            self.current_file_path = file_path
            self.src_img = Image.open(file_path)
            self.update_rect_size() 
            self.refresh_canvas()
            self.rect = self.canvas.create_rectangle(0, 0, self.rect_w * self.scale, self.rect_h * self.scale, outline='red', width=2)
            self.limit_and_move(0, 0)
        except Exception as e:
            messagebox.showerror("Error", f"画像を開けませんでした: {e}")

    def on_window_resize(self, event):
        if self.src_img and self.rect:
            coords = self.canvas.coords(self.rect)
            rx, ry = coords[0] / self.scale, coords[1] / self.scale
            self.refresh_canvas()
            self.limit_and_move(rx * self.scale, ry * self.scale)

    def refresh_canvas(self):
        if not self.src_img: return
        self.root.update_idletasks()
        cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()
        if cw < 10 or ch < 10: return

        self.scale = min(cw / self.src_img.width, ch / self.src_img.height, 1.0)
        new_w, new_h = int(self.src_img.width * self.scale), int(self.src_img.height * self.scale)
        resized_img = self.src_img.resize((new_w, new_h), Image.LANCZOS)
        self.display_img = ImageTk.PhotoImage(resized_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_img)
        self.rect = self.canvas.create_rectangle(0, 0, self.rect_w * self.scale, self.rect_h * self.scale, outline='red', width=2)

    def on_click(self, event):
        if not self.rect: return
        self.start_x, self.start_y = event.x, event.y
        self.limit_and_move(event.x - (self.rect_w * self.scale) // 2, event.y - (self.rect_h * self.scale) // 2)

    def move_rect(self, event):
        if self.rect:
            coords = self.canvas.coords(self.rect)
            new_x = coords[0] + (event.x - self.start_x)
            new_y = coords[1] + (event.y - self.start_y)
            self.limit_and_move(new_x, new_y)
            self.start_x, self.start_y = event.x, event.y

    def limit_and_move(self, x, y):
        if not self.rect or not self.src_img: return
        dw, dh = self.src_img.width * self.scale, self.src_img.height * self.scale
        rw, rh = self.rect_w * self.scale, self.rect_h * self.scale
        if x < 0: x = 0
        elif x + rw > dw: x = dw - rw
        if y < 0: y = 0
        elif y + rh > dh: y = dh - rh
        self.canvas.coords(self.rect, x, y, x + rw, y + rh)

    def save_crop(self):
        if not self.rect or not self.src_img: return
        coords = self.canvas.coords(self.rect)
        rx, ry = int(coords[0] / self.scale), int(coords[1] / self.scale)
        cropped = self.src_img.crop((rx, ry, rx + self.rect_w, ry + self.rect_h))
        base, ext = os.path.splitext(self.current_file_path)
        save_path = filedialog.asksaveasfilename(initialfile=f"{os.path.basename(base)}_crop{ext}", defaultextension=ext)
        if save_path:
            cropped.save(save_path)
            messagebox.showinfo("完了", "保存しました")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ScaledPictCutterV4(root)
    root.mainloop()