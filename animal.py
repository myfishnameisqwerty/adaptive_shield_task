from dataclasses import dataclass
import logging
from typing import Dict
from logger import get_logger
import os
import requester


logger = get_logger("animal", logging.WARNING)


@dataclass
class Animal:
    name: str
    link: str
    picture_local_link: str | None = None
    
    def __str__(self) -> str:
        return self.name
    
    def __dict__(self) -> Dict[str, str]:
        return {self.name: self.picture_local_link}
    
    async def save_picture(self, source: str):
        try:        
            picture_content = await requester.download_image_async("https:"+source)
            if picture_content:
                img_ext = source.split(".")[-1]
                file_name = f"{self.name.replace(' ', '_')}.{img_ext}"
                local_path = os.path.join("tmp", file_name)
                with open(local_path, 'wb') as file:
                    file.write(picture_content)
                    self.picture_local_link = local_path
                    logger.info(f"Picture saved for {self.name} at {local_path}")
        except Exception as e:
            logger.error(e, exc_info=True)