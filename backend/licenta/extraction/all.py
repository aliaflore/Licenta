import pandas as pd
from licenta.extraction.sorting import (
    MAX_VALUE_COLUMN,
    MIN_VALUE_COLUMN,
    RESULT_COLUMN,
    concatenate_by_line,
    create_table,
    group_data_by_line,
    parse_categories,
)
from licenta.extraction.extraction import extract_page_info, filter_only_data_in_table
from licenta.models import AnalysisProvider
import pymupdf


def extract_data_from_pdf(provider: AnalysisProvider, pdf: pymupdf.Document):
    tables = []

    for page in pdf:
        data = extract_page_info(provider, page)
        filtered_data = filter_only_data_in_table(provider, page, data)
        grouped_data = group_data_by_line(provider, filtered_data)
        lines = concatenate_by_line(provider, grouped_data)
        parsed_data = parse_categories(provider, lines)
        final_data = create_table(provider, parsed_data)
        tables.append(final_data)

    final_table = pd.concat(tables)
    final_table.index = range(1, len(final_table) + 1)
    final_table[MIN_VALUE_COLUMN] = final_table[MIN_VALUE_COLUMN].astype(float)
    final_table[MAX_VALUE_COLUMN] = final_table[MAX_VALUE_COLUMN].astype(float)
    final_table[RESULT_COLUMN] = final_table[RESULT_COLUMN].str.replace("=", "")
    final_table[RESULT_COLUMN] = final_table[RESULT_COLUMN].str.strip()

    return final_table
