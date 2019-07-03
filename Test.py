import flask
import os
import requests
from PIL import Image
from io import BytesIO


def save_symbolic(src: str, dst: str):
    return os.symlink(src, dst)


def del_symbolic(file_path: str):
    assert os.path.islink(file_path)
    os.remove(file_path)


def send_image(file_path: str):
    return flask.send_file(file_path, mimetype='image/png')


def sync_images(dir_path: str):
    """
    Sends images in the directory to server, synchronously.
    :param dir_path: path of the folder having symbolic links to non-synchronized images.
    """
    # if the is no file mkdir file.

    for file in os.listdir(dir_path):
        yield send_image(file)
        del_symbolic(file)
        utils.logger.info("Synchronizing... [Image: {0}]".format(file))


# server.py will call this.
def foo(url, header):
    r = requests.get(url, header)
    save_image(Image.open(BytesIO(r.content)))


def save_image(img: Image.Image):
    nf_name = "date"
    f_name = 'three_' + nf_name + '.png'
    img.save('static/data/input' + f_name)
    logger.info('[Image: {0}] successfully downloaded.'.format(f_name))
