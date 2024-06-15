import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

import PyPDF2


SYSTEM_TEXT = """
    Extract the values from this PDF and put them inside a JSON array named results where the objects have the keys 
    "name", "result", "range_min", "range_max", "is_numeric", "expected", "measurement_unit" . Respond just with the JSON object, no other text.
    Inside range_min and range_max print only numbers, no other characters or texts. The result should be a number or the booleans "false" or "true".
    "is_numeric" should be either "true" or "false", depending on the "result". "expected" should be empty if the result is numeric, and should be 
    "false" or "true" if the type is boolean. "measurement_unit" should contain the metric standard notation for the measurement unit for that 
    analysis found in the given text. Translate measurement_unit in English. Do not translate the analysis name. Also put the date of the analysis in the "date" key from the
    parent object.
    """

client = OpenAI(
    organization=os.environ.get("OPENAPI_ORGANIZATION"),
    project=os.environ.get("OPENAPI_PROJECT"),
    api_key=os.environ.get("OPENAPI_KEY"),
)


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text


def createJSON(file):
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_TEXT,
            },
            {"role": "user", "content": extract_text_from_pdf(file)},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(completion.choices[0].message.content)
