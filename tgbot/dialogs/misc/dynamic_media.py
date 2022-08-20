from typing import Optional, Any, Dict, Union

from aiogram_dialog.widgets.text import Text, Const
from aiogram_dialog.manager.manager import DialogManager
from aiogram_dialog.manager.protocols import MediaAttachment, MediaId
from aiogram_dialog.widgets.when import WhenCondition
from aiogram_dialog.widgets.media.base import Media

from aiogram.types import ContentType


def content_type(string: str):
    if string == "text":
        return ContentType.TEXT
    if string == "audio":
        return ContentType.AUDIO
    if string == "animation":
        return ContentType.ANIMATION
    if string == "document":
        return ContentType.DOCUMENT
    if string == "game":
        return ContentType.GAME
    if string == "photo":
        return ContentType.PHOTO
    if string == "sticker":
        return ContentType.STICKER
    if string == "video":
        return ContentType.VIDEO
    if string == "video_note":
        return ContentType.VIDEO_NOTE
    if string == "voice":
        return ContentType.VOICE
    if string == "contact":
        return ContentType.CONTACT
    if string == "venue":
        return ContentType.VENUE
    if string == "location":
        return ContentType.LOCATION
    if string == "poll":
        return ContentType.POLL
    if string == "dice":
        return ContentType.DICE
    if string == "new_chat_members":
        return ContentType.NEW_CHAT_MEMBERS
    if string == "left_chat_member":
        return ContentType.LEFT_CHAT_MEMBER
    return ContentType.UNKNOWN


class DynamicMedia(Media):
    def __init__(
            self,
            *,
            file_id: Union[Text, str, None] = None,
            type: Union[ContentType, Text, str, None] = ContentType.PHOTO,
            media_params: Dict = None,
            when: WhenCondition = None,
    ):
        super().__init__(when)
        if not file_id:
            raise ValueError("File_id is not provided")
        self.type = type
        if isinstance(file_id, str):
            file_id = Const(file_id)
        if isinstance(type, str):
            type = content_type(type)

        self.file_id = file_id
        self.type = type
        self.media_params = media_params or {}

    async def _render_media(
            self,
            data: Any,
            manager: DialogManager
    ) -> Optional[MediaAttachment]:
        if self.file_id:
            file_id = await self.file_id.render_text(data, manager)
        else:
            file_id = None

        if self.type:
            type = await self.type.render_text(data, manager)
        else:
            type = None
        type = content_type(type)

        return MediaAttachment(
            file_id=MediaId(file_id=file_id),
            type=type,
            **self.media_params,
        )


