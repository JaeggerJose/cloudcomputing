from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
# 示例: 将'figlet'文本转换为图像
def text_to_image(text, name):
    width, height = 400, 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Replace spaces in the text with a visual representation (e.g., a dot)
    visual_text = text.replace(' ', '+')

    # Add the visually modified text to the image
    draw.text((10, 10), visual_text, font=font, fill='black', size=20)

    # Save the image to a file
    image.save('/home/ccllab/trainData/' + name + '.png')

    print(f"Image created and saved as {name}.png")


# 获取文件夹中的所有文件

fileList = []
for root, dirs, files in os.walk('/home/ccllab/trainData'):
    for file in files:
        if file.endswith('.txt'):
            fileList.append(file)

# 假设 文件名稱 是你的 'figlet' 文本
for i in fileList:
    
    # text read file
    text = open(i, 'r').read()
    name = i.split('.')[0]
    print(text)
    # 将文本转换为图像
    image_data = text_to_image(text, name)
    # 接下来，你需要将图像数据和对应的标注数据用于模型训练
