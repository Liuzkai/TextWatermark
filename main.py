
import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageDraw, ImageFont

def add_text_watermark(input_folder, output_folder, text, font_size=50, opacity=128):
    # 创建输出文件夹，如果不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 检查文件是否为图片
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # 构建输入和输出文件的完整路径
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)

            # 调用原有的add_text_watermark函数
            add_text_watermark_single_image(input_image_path, output_image_path, text, font_size, opacity)


def add_text_watermark_single_image(input_image_path, output_image_path, text, font_size=50, opacity=128):
    # 创建输出文件夹，如果不存在
    output_folder = os.path.dirname(output_image_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 打开原始图片
    image = Image.open(input_image_path)
    # 将图片转换为RGBA模式
    image = image.convert("RGBA")
    image_width, image_height = image.size

    # 创建一个新的RGBA图像，用于绘制水印
    watermark = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    # 设置字体和颜色
    font = ImageFont.truetype("simfang.ttf", font_size)
    _, _, text_width, text_height = font.getbbox(text)
    color = (0, 0, 0, opacity)

    # 计算水印的起始位置，使其平铺整个图片
    start_x = 0
    start_y = 0
    while start_x< image_width:
        while start_y< image_height:
            draw.text((start_x, start_y), text, fill=color, font=font)
            start_y += text_height * 2
        start_x += text_width * 1.2
        start_y = 0

    # 将水印叠加到原始图片上
    # watermarked_image = Image.alpha_composite(image, watermark)
    image.paste(watermark, (0, 0), watermark )

    image = image.convert("RGB")
    # 保存带有水印的图片
    image.save(output_image_path, quality=90)

def browse_input_folder():
    folder_path = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_path)

def apply_watermark():
    input_folder = input_folder_entry.get()
    output_folder = os.path.join(input_folder, "Output")
    text = watermark_text_entry.get()
    font_size = int(watermark_size_scale.get())
    opacity = int(watermark_opacity_scale.get())

    # 获取输入文件夹中的图片文件数量
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
    total_images = len(image_files)

    # 初始化进度条
    progress_bar['maximum'] = total_images
    progress_bar['value'] = 0

    # 添加水印并更新进度条
    for i, image_file in enumerate(image_files):
        input_image_path = os.path.join(input_folder, image_file)
        output_image_path = os.path.join(output_folder, image_file)
        add_text_watermark_single_image(input_image_path, output_image_path, text, font_size, opacity)

        # 更新进度条
        progress_bar['value'] = i + 1
        root.update()

root = tk.Tk()
root.title("添加水印助手")

input_folder_label = tk.Label(root, text="图片文件夹:")
input_folder_label.grid(row=0, column=0, padx=6, pady=6)

input_folder_entry = tk.Entry(root)
input_folder_entry.grid(row=0, column=1, padx=6, pady=6)

browse_button = tk.Button(root, text="打开路径", command=browse_input_folder)
browse_button.grid(row=0, column=2, padx=6, pady=6)

watermark_text_label = tk.Label(root, text="水印内容:")
watermark_text_label.grid(row=1, column=0, padx=6, pady=6)

watermark_text_entry = tk.Entry(root)
watermark_text_entry.grid(row=1, column=1, padx=6, pady=6)

watermark_size_label = tk.Label(root, text="水印大小:")
watermark_size_label.grid(row=2, column=0, padx=6, pady=6)

watermark_size_scale = tk.Scale(root, from_=0, to=256, orient=tk.HORIZONTAL)
watermark_size_scale.grid(row=2, column=1, padx=6, pady=6)
watermark_size_scale.set(64)

watermark_opacity_label = tk.Label(root, text="水印透明度:")
watermark_opacity_label.grid(row=3, column=0, padx=6, pady=6)

watermark_opacity_scale = tk.Scale(root, from_=0, to=256, orient=tk.HORIZONTAL)
watermark_opacity_scale.grid(row=3, column=1, padx=6, pady=6)
watermark_opacity_scale.set(64)

apply_button = tk.Button(root, text="添加水印", command=apply_watermark)
apply_button.grid(row=4, column=0, columnspan=3, padx=6, pady=6)

# 添加进度条
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.grid(row=5, column=0, columnspan=3, padx=6, pady=10)

root.mainloop()
