import boto3
from botocore.exceptions import ClientError
from app.core.conf import settings
from app.logger import logger


async def get_photo_from_aws(photoId: str) -> bytes | None:
    session = boto3.session.Session()
    try:
        s3 = session.client(
            service_name='s3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        photo = s3.get_object(Bucket='diploma', Key=f'admin/image/{photoId}.png')
        return photo['Body'].read()
    except ClientError as err:
        logger.error("S3 Error (Image): ", err)
        return None


async def get_music_from_aws(musicId: str) -> bytes | None:
    session = boto3.session.Session()
    try:
        s3 = session.client(
            service_name='s3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        photo = s3.get_object(Bucket='diploma', Key=f'admin/music/{musicId}.mp3')
        return photo['Body'].read()
    except ClientError as err:
        logger.error("S3 Error (Music): ", err)
        return None
