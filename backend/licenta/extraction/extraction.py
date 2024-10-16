from licenta.models import AnalysisProvider
import pymupdf
from thefuzz import fuzz
from django.conf import settings
import logging


logger = logging.getLogger(__name__)



def extract_page_info(provider: AnalysisProvider, page: pymupdf.Page):
    pdata = page.get_textpage_ocr(language=settings.TESSERACT_LANGUAGES, flags=8)
    data = [
        (k["text"], k["bbox"], k["flags"])
        for d in pdata.extractDICT(sort=True)["blocks"]
        for j in d["lines"]
        for k in j["spans"]
    ]
    for i in range(len(data)):
        if data[i][0].count("   ") > 1:
            c = list(data[i])
            c[0] = c[0].strip()
            c[1] = list(c[1])
            c[1][0] += (len(data[i][0]) - len(c[0])) * provider.space_pixels
            c[1] = tuple(c[1])
            data[i] = tuple(c)
    return data


def filter_only_data_in_table(provider: AnalysisProvider, page: pymupdf.Page, data: list):
    crop_x_min = provider.crops_pixels.get("left", 0)
    crop_y_min = provider.crops_pixels.get("top", 0)
    crop_x_max = page.mediabox[2] - provider.crops_pixels.get("right", 0)
    crop_y_max = page.mediabox[3] - provider.crops_pixels.get("bottom", 0)

    all_strings = set([v for crop_type in provider.crops_words.values() for v in crop_type])

    for search_word in all_strings:
        for text, bbox, _ in data:
            ratio = fuzz.partial_ratio(search_word, text)
            if ratio > provider.crop_similarity and len(search_word) <= len(text):
                logger.debug(f"Found {search_word} in {text} at {bbox=} with {ratio=}")
                word_top = bbox[1]
                word_left = bbox[0]
                word_right = bbox[2]
                word_bottom = bbox[3]

                if search_word in provider.crops_words.get("top", []):
                    crop_y_min = max(crop_y_min, word_bottom)
                elif search_word in provider.crops_words.get("bottom", []):
                    crop_y_max = min(crop_y_max, word_top)
                elif search_word in provider.crops_words.get("left", []):
                    crop_x_min = max(crop_x_min, word_right)
                elif search_word in provider.crops_words.get("right", []):
                    crop_x_max = min(crop_x_max, word_left)

    filtered_data = list(
        filter(
            lambda x: x[1][0] >= crop_x_min
            and x[1][1] >= crop_y_min
            and x[1][2] <= crop_x_max
            and x[1][3] <= crop_y_max,
            data,
        )
    )
    filtered_data = list(
        filter(lambda x: x[0] not in provider.ignored_words, filtered_data)
    )

    return filtered_data
