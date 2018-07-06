from django.utils.crypto import get_random_string

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
