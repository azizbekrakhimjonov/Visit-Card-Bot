from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os

def create_visitCard(fullname: str, job: str, phone: str, email: str, address: str, website: str):
    img1 = Image.open(r'1.png')
    img2 = Image.open(f"{fullname}.jpg")


    width, height = img2.size
    left = 0
    top = width / 70
    right = width
    bottom = height
    m = img2.crop((top, left, right, bottom))

    weight = 320
    aspect_ratio = m.width / m.height
    new_height = int(weight / aspect_ratio)
    img2 = m.resize((weight, new_height))

    hexagon_size = (320, 370)  # 320
    mask_im = Image.new("L", img2.size, 0)

    draw = ImageDraw.Draw(mask_im)
    draw.polygon([(hexagon_size[0] // 2, 0), (hexagon_size[0], hexagon_size[1] // 4),
                  (hexagon_size[0], 3 * hexagon_size[1] // 4), (hexagon_size[0] // 2, hexagon_size[1]),
                  (0, 3 * hexagon_size[1] // 4), (0, hexagon_size[1] // 4)], fill=255)

    kichik_rasim = Image.composite(img2, Image.new("RGBA", img2.size), mask_im)  # keraksiz tomonlarni olib tashlash
    img1 = img1.copy()
    img1.paste(kichik_rasim, (78, 66), mask_im)  # set hexagon avatar idCard

    draw = ImageDraw.Draw(img1)
    font = ImageFont.truetype("regular.ttf", 50)
    draw.text((506, 110), fullname, (0, 0, 0), font=font)
    draw.text((506, 166), job, (0, 0, 0), font=font)

    font = ImageFont.truetype("regular.ttf", 25)
    draw.text((550, 285), phone, (0, 0, 0), font=font)
    draw.text((550, 332), email, (0, 0, 0), font=font)
    draw.text((550, 381), address, (0, 0, 0), font=font)
    draw.text((550, 425), website, (0, 0, 0), font=font)

    # os.system(f'rm {fullname}.png')

    img1.save(f'{fullname}.png')

# create_visitCard("Azizbek Rahimjonov", "Developer", "+998 (93) 260-80-05",
#                  "azizbekrahimjonov571@swagger.uz", "USA", "www.swagger.uz")


