from django.utils.crypto import get_random_string
import qrcode
from PIL import Image
import os

def image_rename(instance, filename):
    """
    对上传的图片进行重命名
    :param instance: 
    :param filename: 
    :return: 图片的路径和名字
    """
    # file will be uploaded to MEDIA_ROOT/image/id_string_filename
    return 'image/{0}_{1}_{2}'.format(instance.id, get_random_string(), filename)


def delete_image(product_info_obj, attr_name):
    """
    删除图片
    :param product_info_obj: 
    :param attr_name: 
    :return: 删除成功：true; 失败：false
    """
    fish_info_obj = product_info_obj.fish_info
    process_info_obj = product_info_obj.process_info

    try:
        if attr_name == "pack_environment":
            process_info_obj.pack_environment.delete()
        elif attr_name == "test_report_stock":
            fish_info_obj.test_report_stock.delete()
        elif attr_name == "test_report_third":
            fish_info_obj.test_report_third.delete()
        elif attr_name == "stock_scene":
            fish_info_obj.stock_scene.delete()
        elif attr_name == "process_environment":
            process_info_obj.process_environment.delete()
        elif attr_name == "get_scene":
            process_info_obj.get_scene.delete()
        elif attr_name == "test_report_process":
            process_info_obj.test_report_process.delete()
    except Exception:
        return False
    return True


def create_qrcode(url, filename):
    """
    :param url: 二维码中包含的路径
    :param filename: 二维码保存的文件名
    :return: 二维码图片
    """
    qr = qrcode.QRCode(
        version=1,
        # 设置容错率为最高
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=10,  # 二维码大小
        border=2,  # 边框大小
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()
    # 设置二维码为彩色
    img = img.convert("RGBA")
    icon = Image.open(os.getcwd() + "/media/image/" + 'logo.png')
    w, h = img.size
    factor = 4
    size_w = int(w / factor)
    size_h = int(h / factor)
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    w = int((w - icon_w) / 2)
    h = int((h - icon_h) / 2)
    icon = icon.convert("RGBA")
    newimg = Image.new("RGBA", (icon_w + 8, icon_h + 8), (255, 255, 255))
    img.paste(newimg, (w - 4, h - 4), newimg)

    img.paste(icon, (w, h), icon)
    img.save(os.getcwd() + "/media/image/" + filename + '.png', quality=100)

    return img


# if __name__ == '__main__':
#     create_qrcode("http//:baidu.com", "qrcode")