import os
from datetime import datetime
from secrets import token_hex

from werkzeug.utils import secure_filename

path = os.path.abspath(os.path.dirname(__file__))
upload_path = os.path.join(path, '..', 'uploads')


def save_image_upload(image):
    date_format = "%Y%m%dT%H%M%S"
    now = datetime.utcnow().strftime(date_format)
    random_string = token_hex(2)
    filename = random_string + "_" + now + "_" + image.data.filename
    filename = secure_filename(filename)
    image.data.save(os.path.join(upload_path, filename))
    return filename
