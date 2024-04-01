from PIL import Image, ImageDraw, ImageFont

# 创建一个空白图像
width, height = 100, 100
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# 设置字体和大小
font = ImageFont.truetype("arial.ttf", 80)

# 设置字符和颜色
char = "X"
color = "black"

# 计算字符的宽度和高度
text_width, text_height = draw.textsize(char, font=font)

# 计算字符的位置
x = (width - text_width) / 2
y = (height - text_height) / 2

# 在图像上绘制字符
draw.text((x, y), char, font=font, fill=color)

# 保存图像
image.save("icon.png")
