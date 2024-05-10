import cv2
import numpy as np
import face_recognition
from typing import List
from numpy import ndarray
from pydantic import BaseModel, ConfigDict


class Face(BaseModel):
    data: np.ndarray
    model_config = ConfigDict(arbitrary_types_allowed=True)


def resize_image(faceImage: ndarray) -> ndarray:
    resizedImage = cv2.resize(faceImage, (48, 48))
    preprocImage: ndarray = np.array(resizedImage) / 255
    preprocImage = np.array([preprocImage])
    return preprocImage


def find_faces(photo: bytes) -> List[Face] | None:
    """
    Find first face on photo and resize it to 60x60 pixels
    :param photo:
    :return List[Face]:
    """
    npArray = np.frombuffer(photo, np.uint8)
    image = cv2.imdecode(npArray, cv2.IMREAD_COLOR)
    faces = face_recognition.face_locations(image)
    if len(faces) == 0:
        return None
    return [Face(data=resize_image(image[face[0]:face[2], face[3]:face[1]])) for face in faces]
