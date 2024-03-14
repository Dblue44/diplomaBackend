import cv2
import numpy as np
import face_recognition
from typing import List
from numpy import ndarray
from pydantic import BaseModel, ConfigDict


faceProto = "C:/Users/stakh/Models/opencv_face_detector.pbtxt"
faceModel = "C:/Users/stakh/Models/opencv_face_detector_uint8.pb"
ml = cv2.dnn.readNet(faceModel, faceProto)


class Face(BaseModel):
    data: np.ndarray
    model_config = ConfigDict(arbitrary_types_allowed=True)


def resize_image(faceImage: ndarray) -> ndarray:
    resizedImage = cv2.resize(faceImage, (60, 60))
    preprocImage: ndarray = np.array(resizedImage) / 255
    return preprocImage


def find_faces(photo: bytes) -> List[Face]:
    npArray = np.frombuffer(photo, np.uint8)
    image = cv2.imdecode(npArray, cv2.IMREAD_COLOR)
    faces = face_recognition.face_locations(image)
    faceImages = []
    for face in faces:
        faceImage = image[face[0]:face[2], face[3]:face[1]]
        resizedFaceImage = resize_image(faceImage)
        faceImages.append(Face(data=resizedFaceImage))
    return faceImages
