import os

import numpy as np
from dotenv import load_dotenv
from image_processing import deskew
from ocr import extract_text_from_image
from openai import OpenAI
import json
from reading import pages

load_dotenv()

import PyPDF2


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text


# Create a list to store extracted text from all pages
# extracted_text = []

# for page in pages:
#     preprocessed_image = deskew(np.array(page))

#     text = extract_text_from_image(preprocessed_image)
#     extracted_text.append(text)


client = OpenAI(
    organization=os.environ.get("OPENAPI_ORGANIZATION"),
    project=os.environ.get("OPENAPI_PROJECT"),
    api_key=os.environ.get("OPENAPI_KEY"),
)

file_name = "synevo/synevo/78d7e7db-ec1f-452f-9408-5846c32f7001.pdf"

SYSTEM_TEXT = """
Extract the values from this PDF and put them inside a JSON array named results where the objects have the keys 
"analysis", "result", "range_min", "range_max", "type", "expected", "measurement_unit" . Respond just with the JSON object, no other text.
Inside range_min and range_max print only numbers, no other characters or texts. The result should be a number or the booleans "false" or "true".
type should be either "boolean" or "interval". expected should be empty if the type is interval, and should be "false" or "true" if the type is boolean.
measurement_unit should contain the metric standard notation for the measurement unit for that analysis. Translate measurement_unit in English.
Do not translate the analysis name.
"""

completion = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_TEXT,
        },
        {"role": "user", "content": extract_text_from_pdf(file_name)},
    ],
    response_format={"type": "json_object"},
)

print(json.loads(completion.choices[0].message.content))
