from celery import shared_task
from django.conf import settings
from licenta.models import AnalizePDF, Analize, AnalizeRezultate, User
from licenta.extraction.text_extraction import createJSON
import logging
import datetime

logger = logging.getLogger(__name__)


@shared_task
def analyze_pdf(pdf_id: int, user_id: int):

    pdf = AnalizePDF.objects.get(id=pdf_id)
    user = User.objects.get(id=user_id)

    analiza = Analize.objects.create(source=pdf, user=user)

    results = createJSON(pdf.file.file)

    analiza.date = datetime.datetime.fromisoformat(results["date"])
    analiza.save()

    for result in results["results"]:
        try:
            r_min = float(result.get("range_min")) if result.get("range_min") else None
        except ValueError:
            r_min = None

        try:
            r_max = float(result.get("range_max")) if result.get("range_max") else None
        except ValueError:
            r_max = None

        is_numeric = result.get("is_numeric") in ["true", "True", "1", True]
        measurement_unit = result.get("measurement_unit", "")
        name = result.get("name")

        if is_numeric:
            try:
                r_result = float(result.get("result", 0))
            except ValueError:
                r_result = 0.0
            r_expected = None
        else:
            r_expected = result.get("expected") in ["true", "True", "1", True]
            r_result = float(result.get("result") in ["true", "True", "1", True])

        try:
            r = AnalizeRezultate.objects.create(
                name=name,
                is_numeric=is_numeric,
                result=r_result,
                range_min=r_min,
                range_max=r_max,
                expected=r_expected,
                measurement_unit=measurement_unit,
                analysis=analiza,
            )

            if r.is_numeric:
                if (r.range_min and r.result < r.range_min) or (r.range_max and r.result > r.range_max):
                    add_suggestion.delay(r.id, True)
            else:
                if r.result != r.expected:
                    add_suggestion.delay(r.id, False)
        except Exception as e:
            print(e)

SUGGESTION_PROMPT_NUMERIC = "Suggest a fix for the analysis `%s`. The result is `%s` and it should be between `%s` and `%s`. The measurement unit is `%s`. Please provide a suggestion in English about what the user should do."
SUGGESTION_PROMPT_NON_NUMERIC = "Suggest a fix for the analysis `%s`. The result is `%s` and it should be `%s`. The measurement unit is `%s`. Please provide a suggestion in English about what the user should do."

@shared_task
def add_suggestion(result_id: int, numeric: bool):
    result = AnalizeRezultate.objects.get(id=result_id)

    prompt = SUGGESTION_PROMPT_NUMERIC if numeric else SUGGESTION_PROMPT_NON_NUMERIC

    suggestion = settings.OPENAPI_CLIENT.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt % (result.name, result.result, result.range_min, result.range_max, result.measurement_unit),
            },
        ],
    )

    logger.info("Suggestion added for analysis %s", result.name)

    result.suggestion = suggestion.choices[0].message.content
    result.save()
