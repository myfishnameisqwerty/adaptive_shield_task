import asyncio
from requester import fetch, download_image_async


PAGE_URL = "https://en.wikipedia.org/wiki/Antelope"
IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Blackbuck_male_female.jpg/220px-Blackbuck_male_female.jpg"


async def test_fetch():
    # Test fetching a web page
    page_content = await fetch(PAGE_URL)
    assert page_content is not None
    assert "<title>Antelope" in page_content


async def test_download_image_async():
    # Test downloading an image
    image_content = await download_image_async(IMAGE_URL)
    assert image_content is not None
    assert isinstance(image_content, bytes)
    assert len(image_content) > 0

# Run the tests
if __name__ == "__main__":
    asyncio.run(test_fetch())
    asyncio.run(test_download_image_async())
