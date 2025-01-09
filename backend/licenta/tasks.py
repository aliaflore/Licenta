import decimal
import logging
from io import StringIO

import pandas as pd
import pymupdf
import requests
from celery import shared_task
from django.conf import settings
from django.db import transaction
from licenta.category_import import CategoryImportMatcher, PDFCategoryImporter, TranslatedCategoryImport
from licenta.extraction.all import extract_data_from_pdf
from licenta.extraction.sorting import (CATEGORY_COLUMN, MAX_VALUE_COLUMN,
                                        MEASURE_UNIT_COLUMN, MIN_VALUE_COLUMN,
                                        NAME_COLUMN, REF_RANGE_COLUMN,
                                        RESULT_COLUMN, IN_RANGE_COLUMN)
from licenta.models import (Analysis, AnalysisCategory, AnalysisCategoryName,
                            AnalysisPDF, AnalysisProvider, AnalysisResult)

logger = logging.getLogger(__name__)

SUGGESTION_PROMPT = "Suggest a fix for the analysis `%s`. The result is `%s` and it should be between `%s` and `%s`. The measurement unit is `%s`. Please provide a suggestion in English about what the user should do."


@shared_task
@transaction.atomic
def analyze_pdf(analysis_pk):
    analysis_pdf = AnalysisPDF.objects.get(pk=analysis_pk)
    Analysis.objects.filter(source=analysis_pdf).delete()
    analysis = Analysis.objects.create(source=analysis_pdf)
    pdf = pymupdf.Document(stream=analysis_pdf.file.open("rb").read())

    data = extract_data_from_pdf(analysis_pdf.provider, pdf)

    categories_names = list(AnalysisCategoryName.objects.filter(
        pk__in=data[CATEGORY_COLUMN].unique()
    ).all())

    results = []
    for _, row in data.iterrows():
        result = AnalysisResult(
            category=next(
                c_name.category for c_name in categories_names if c_name.pk == row[CATEGORY_COLUMN]
            ),
            name=row[NAME_COLUMN].strip(),
            result=row[RESULT_COLUMN].strip(),
            measurement_unit=str(row[MEASURE_UNIT_COLUMN]).strip(),
            refference_range=str(row[REF_RANGE_COLUMN]).strip(),
            range_min=decimal.Decimal(row[MIN_VALUE_COLUMN]) if not pd.isna(row[MIN_VALUE_COLUMN]) else None,
            range_max=decimal.Decimal(row[MAX_VALUE_COLUMN]) if not pd.isna(row[MAX_VALUE_COLUMN]) else None,
            in_range=bool(row[IN_RANGE_COLUMN]) if not pd.isna(row[IN_RANGE_COLUMN]) else None,
            analysis=analysis,
        )
        results.append(result)

    AnalysisResult.objects.bulk_create(results)


@shared_task
@transaction.atomic
def add_suggestion(result_pk: int):
    result = AnalysisResult.objects.get(pk=result_pk)

    suggestion = settings.OPENAPI_CLIENT.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": SUGGESTION_PROMPT
                % (
                    result.name,
                    result.result,
                    result.range_min,
                    result.range_max,
                    result.measurement_unit,
                ),
            },
        ],
    )

    logger.info("Suggestion added for analysis %s", result.name)

    result.suggestion = suggestion.choices[0].message.content
    result.save()


@shared_task
@transaction.atomic
def update_all_analysis_categories():
    AnalysisCategory.objects.all().delete()
    response = requests.get(
        "https://docs.google.com/spreadsheets/d/12rEWTwolEPUCIuWieY94XeK7vsOMZeia1KVkdWzBFwA/export?format=csv&gid=0"
    )
    assert response.status_code == 200, "Wrong status code"
    categories_df = pd.read_csv(StringIO(response.text))

    categories = {}
    for row in categories_df.iloc:
        synonims = list(filter(lambda x: not isinstance(x, float), row[1:]))
        if len(synonims) == 0:
            continue
        base = synonims[0]
        categories[base] = synonims

    created_categories = AnalysisCategory.objects.bulk_create(
        [AnalysisCategory(name=base) for base in categories.keys()]
    )
    analysis_names = []
    for created_category, synonims in zip(created_categories, categories.values()):
        analysis_names.extend(
            [
                AnalysisCategoryName(name=synonim, category=created_category)
                for synonim in synonims
            ]
        )
    AnalysisCategoryName.objects.bulk_create(analysis_names)


@shared_task
def import_all_analysis_categories():
    provider_data = []
    for provider in AnalysisProvider.objects.all():
        importer = PDFCategoryImporter(provider)
        importer.provide()
        translated_importer = TranslatedCategoryImport(importer)
        translated_importer.provide()
        provider_data.append(translated_importer)
    with transaction.atomic():
        matcher = CategoryImportMatcher(provider_data)
        groups = matcher.match()
        for group in groups:
            category, _  = AnalysisCategory.objects.get_or_create(name=group[0][1])
            for name in group:
                AnalysisCategoryName.objects.get_or_create(name=name[1], category=category)
