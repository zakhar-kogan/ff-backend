from pathlib import Path

with open("test.jpg", "rb") as image_file:
    img = image_file.read()

from modal import ocr_content


async def test_ocr_content():
    ocr_result = await ocr_content(img, "en")

    return ocr_result


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_ocr_content(), debug=True)
