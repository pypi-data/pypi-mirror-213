import tempfile
from typing import Optional, Union

import cv2


def generate_thumbnail(video_link: Union[str, bytes]) -> Optional[bytes]:
    if isinstance(video_link, bytes):
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(video_link)
            video_link = temp.name

    cam = cv2.VideoCapture(video_link)

    ret, frame = cam.read()
    if ret:
        b = cv2.imencode('.jpg', frame)[1].tobytes()
        return b
