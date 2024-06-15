from celery import shared_task
from licenta.models import AnalizePDF, Analize, AnalizeRezultate, User
from licenta.extraction.text_extraction import createJSON
import logging
import datetime

logger = logging.getLogger(__name__)


@shared_task
def analyze_pdf(pdf_id: int, user_id: int):

    pdf = AnalizePDF.objects.get(id=pdf_id)
    user = User.objects.get(id=user_id)

    pdf.file.file

    analiza = Analize.objects.create(source=pdf, user=user)

    results = createJSON(pdf.file.file)

    analiza.date = datetime.datetime.fromisoformat(results["date"])
    analiza.save()

    for result in results["results"]:
        print(result)
        r_min = result.get("range_min")
        if r_min == "":
            r_min = None

        r_max = result.get("range_max")
        if r_max == "":
            r_max = None

        r_result = result.get("is_numeric")
        if r_result == "":
            r_result = 0

        r_expected = result.get("expected")
        if r_result == "false":
            r_result = False
        elif r_result == "true":
            r_result = True
        try:
            AnalizeRezultate.objects.create(
                name=result.get("name"),
                is_numeric=result.get("is_numeric"),
                result=float(r_result),
                range_min=r_min,
                range_max=r_max,
                expected=r_expected,
                measurement_unit=result.get("measurement_unit"),
                analysis=analiza,
            )
        except Exception as e:
            print(e)
