import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# --- 配置区 ---
BASE_URL = "https://你的域名/postman.html"  # 替换成你部署后的实际地址
ROLES = [
    "1号位-原配", "2号位-闺蜜", "3号位-初恋", "4号位-邻居",
    "5号位-渣男", "6号位-兄弟", "7号位-律师", "8号位-管家"
]
OUTPUT_DIR = "qr_codes"

# 创建输出文件夹
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_custom_qr(role_index, role_name):
    # 1. 构造带参数的 URL
    target_url = f"{BASE_URL}?id={role_index}"
    
    # 2. 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(target_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # 3. 在下方添加文字标注（使用 Pillow）
    width, height = qr_img.size
    canvas = Image.new('RGB', (width, height + 50), 'white')
    canvas.paste(qr_img, (0, 0))
    
    draw = ImageDraw.Draw(canvas)
    # Mac 系统自带的中文字体路径（如果报错，请检查路径）
    font_path = "/System/Library/Fonts/PingFang.ttc" 
    try:
        font = ImageFont.truetype(font_path, 24)
    except:
        font = ImageFont.load_default()
        
    # 计算文字居中位置
    text_bbox = draw.textbbox((0, 0), role_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text(((width - text_width) // 2, height - 10), role_name, fill="black", font=font)
    
    # 4. 保存
    file_name = f"role_{role_index}.png"
    canvas.save(os.path.join(OUTPUT_DIR, file_name))
    print(f"已生成: {file_name} -> {role_name}")

# 执行生成
for index, name in enumerate(ROLES):
    generate_custom_qr(index, name)

print(f"\n✅ 所有二维码已保存在 {OUTPUT_DIR} 文件夹中！")