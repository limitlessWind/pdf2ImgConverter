import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image

# 创建一个Tkinter窗口
root = tk.Tk()
root.title("PDF转图像转换器")

# 设置窗口的宽度和高度
window_width = 600  # 设置窗口宽度
window_height = 400  # 设置窗口高度

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口的x和y坐标，使其居中
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# 设置窗口的几何属性
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 用于存储所选的PDF文件列表
selected_pdf_files = []

# 用于显示所选的PDF文件列表
pdf_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=150, height=10)
pdf_listbox.pack()

# 函数：添加PDF文件到列表
def add_pdf_files():
    files = filedialog.askopenfilenames(title="选择输入PDF文件", filetypes=[("PDF Files", "*.pdf")])
    for file in files:
        selected_pdf_files.append(file)
        pdf_listbox.insert(tk.END, os.path.basename(file))

# 按钮：添加PDF文件
add_files_button = tk.Button(root, text="添加PDF文件", command=add_pdf_files)
add_files_button.pack()

# 用于显示输出文件夹的路径
output_folder_label = tk.Label(root, text="")
output_folder_label.pack()

# 函数：选择输出文件夹
def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory(title="选择输出文件夹")
    if output_folder:
        output_folder_label.config(text=f"输出文件夹: {output_folder}")
        # convert_to_images(output_folder)

# 按钮：选择输出文件夹
output_folder_button = tk.Button(root, text="选择输出文件夹", command=select_output_folder)
output_folder_button.pack()

# 函数：将PDF文件转换为图像
def convert_to_images():    
    if not selected_pdf_files:
        messagebox.showwarning("警告", "没有选择PDF文件")
        return
    if not output_folder:
        messagebox.showwarning("警告", "没有选择PDF输出路径")
        return
    for pdf_file in selected_pdf_files:
        images = convert_from_path(pdf_file)
        if images.__len__() > 1:
            img1_size, img2_size = images[0].size, images[1].size
            width = max([img1_size[0], img2_size[0]])
            height = img1_size[1] + img2_size[1]
            instance = Image.new('RGB', (width, height), (255, 255, 255))  # 创建背景为白色的空图片
            instance.paste(images[0])  # 以坐标(0,0)为基准粘贴第一张图片
            instance.paste(images[1], (0, img1_size[1]))  # 以坐标(0,第一张图片的高)为基准粘贴第二张图片

            # for image in images[1:]:
            #     merged_image.paste(image, (merged_image.size[1], 0))
            file_name = os.path.splitext(os.path.basename(pdf_file))[0]
            output_filename = os.path.join(output_folder, f'{file_name}.jpg')
            # 保存合并后的图像
            instance.save(output_filename, 'JPEG')
        else:  
            merged_image = images[0]  # 使用第一页作为起始图像
            # for image in images[1:]:
            #     merged_image.paste(image)
            file_name = os.path.splitext(os.path.basename(pdf_file))[0]
            output_filename = os.path.join(output_folder, f'{file_name}.jpg')
            # 保存合并后的图像
            merged_image.save(output_filename, 'JPEG')
    selected_pdf_files.clear()
    pdf_listbox.delete(0, tk.END)
    show_conversion_complete_message()

# 函数：显示转换完成提示
def show_conversion_complete_message():
    messagebox.showinfo("转换完成", "PDF文件已成功转换为图像")

# 创建一个框架以容纳按钮，并将其放在底部的中间位置
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=50)
convert_button = tk.Button(button_frame, text="开始转换", command=convert_to_images)
convert_button.pack(side=tk.LEFT)  # 将按钮放在框架的左侧

# 运行Tkinter主循环
root.mainloop()
