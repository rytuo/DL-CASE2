from fastapi import Header

from core.settings import settings


async def valid_content_length(content_length: int = Header(..., lt=settings.MAX_FILE_SIZE, include_in_schema=False)):
    return content_length
