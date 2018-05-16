from django.utils.crypto import get_random_string

def image_rename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/image/id_string_filename
    return 'image/{0}_{1}_{2}'.format(instance.user.id, get_random_string(), filename)
