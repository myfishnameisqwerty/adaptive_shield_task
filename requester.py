from logger import get_logger
import aiohttp
import logging


logger = get_logger("requester", logging.WARNING)


async def fetch(url: str) -> str | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()

    except aiohttp.ClientError as e:
        logger.warning(f"Fetching failed to {url}: {e}.")

    except Exception as e:
        logger.error(f"Error {e} raiser on fetch attempt.")


async def download_image_async(url: str) -> bytes | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                image_content = await response.read()
                logger.info(f"Image downloaded successfully from: {url}")
                return image_content
    except aiohttp.ClientError as e:
        logger.warning(f"Error downloading image: {e}")
    except Exception as e:
        logger.error(f"Error {e} raised on download attempt.")