import os
import shutil
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk

#direktori
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUMBER = os.path.join(BASE_DIR, "foto", "sumber")
BAGUS = os.path.join(BASE_DIR, "foto", "bagus")
LUMAYAN = os.path.join(BASE_DIR, "foto", "lumayan")
JELEK = os.path.join(BASE_DIR, "foto", "jelek")

os.makedirs(SUMBER, exist_ok=True)
os.makedirs(BAGUS, exist_ok=True)
os.makedirs(LUMAYAN, exist_ok=True)
os.makedirs(JELEK, exist_ok=True)

#ekstensi gambar
EXTENSIONS = (".jpg", ".jpeg", ".png")
files = [f for f in os.listdir(SUMBER) if f.lower().endswith(EXTENSIONS)]
total = len(files)
index = 0

#undo
history = []

#ukuran window
THUMB_SIZE = (600, 600)

#function
def load_image():
  global img_tk

  if index >= total:
    root.after(500, root.destroy)
    return

  path = os.path.join(SUMBER, files[index])

  img = Image.open(path)
  img.thumbnail(THUMB_SIZE)

  canvas = Image.new("RGB", THUMB_SIZE, (240, 240, 240))
  x = (THUMB_SIZE[0] - img.width) // 2
  y = (THUMB_SIZE[1] - img.height) // 2
  canvas.paste(img, (x, y))

  img_tk = ImageTk.PhotoImage(canvas)
  img_label.config(image=img_tk)

  counter_label.config(text=f"Foto {index + 1} / {total}")

def move_to(folder):
  global index

  if index >= total:
    return

  filename = files[index]
  src = os.path.join(SUMBER, filename)
  dst = os.path.join(folder, filename)

  shutil.move(src, dst)
  history.append((filename, folder))

  index += 1
  load_image()

def undo():
  global index

  if not history or index <= 0:
    return

  filename, folder = history.pop()
  src = os.path.join(folder, filename)
  dst = os.path.join(SUMBER, filename)

  shutil.move(src, dst)
  index -= 1
  load_image()

#sortcut
def key_handler(event):
  if event.char == "1":
    move_to(BAGUS)
  elif event.char == "2":
    move_to(LUMAYAN)
  elif event.char == "3":
    move_to(JELEK)
  elif event.state & 0x4 and event.keysym.lower() == "z":
    undo()

#gui
root = Tk()
root.title("Sortir Foto")

root.bind("<Key>", key_handler)

counter_label = Label(root, font=("Arial", 12))
counter_label.pack(pady=5)

img_label = Label(root)
img_label.pack(pady=10)

btn_frame = Frame(root)
btn_frame.pack(pady=5)

Button(btn_frame, text="Bagus (1)", width=15,
  command=lambda: move_to(BAGUS)).grid(row=0, column=0, padx=5)

Button(btn_frame, text="Lumayan (2)", width=15,
  command=lambda: move_to(LUMAYAN)).grid(row=0, column=1, padx=5)

Button(btn_frame, text="Jelek (3)", width=15,
  command=lambda: move_to(JELEK)).grid(row=0, column=2, padx=5)

Button(btn_frame, text="Undo (Ctrl+Z)", width=15,
  command=undo).grid(row=1, column=1, pady=8)

load_image()
root.mainloop()