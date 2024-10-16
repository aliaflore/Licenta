from collections import defaultdict
from thefuzz import fuzz
import io
import pandas as pd
import re
import numpy as np

from licenta.models import AnalysisCategoryName, AnalysisProvider


CATEGORY_COLUMN = "Category"
NAME_COLUMN = "Name"
RESULT_COLUMN = "Result"
MEASURE_UNIT_COLUMN = "Measurement Unit"
REF_RANGE_COLUMN = "Refference Range"
MIN_VALUE_COLUMN = "Minimum Value"
MAX_VALUE_COLUMN = "Maximum Value"
IN_RANGE_COLUMN = "In Range"
COLUMN_NAMES = [
    CATEGORY_COLUMN,
    NAME_COLUMN,
    RESULT_COLUMN,
    MEASURE_UNIT_COLUMN,
    REF_RANGE_COLUMN,
    MIN_VALUE_COLUMN,
    MAX_VALUE_COLUMN,
    IN_RANGE_COLUMN,
]


def group_data_by_line(provider: AnalysisProvider, data: list):
    grouped_data = defaultdict(list)

    for word_info in data:
        _, (_, top, _, _), _ = word_info
        found = False
        for key in grouped_data:
            if abs(top - key) <= provider.line_height_tolerance:
                grouped_data[key].append(word_info)
                found = True
                break
        if not found:
            grouped_data[top].append(word_info)

    for k, v in grouped_data.items():
        grouped_data[k] = sorted(v, key=lambda x: x[1][0])

    new_data = []
    for i, line in enumerate(grouped_data.values()):
        if i == 0:
            new_data.append(line)
            continue
        first_word_new_line = line[0]
        first_word_last_line = new_data[-1][0]
        if (
            first_word_new_line[1][0] - first_word_last_line[1][0]
            >= provider.line_continuation_difference_width
            or first_word_new_line[2] & 2**1
        ):
            removed_italics = list(filter(lambda x: not x[2] & 2**1, line))
            new_data[-1].extend(removed_italics)
        else:
            new_data.append(line)

    def compare_words(word1, word2):
        if (
            word1[1][1] - provider.word_width_tolerance
            <= word2[1][1]
            <= word1[1][1] + provider.word_width_tolerance
        ):
            return word1[1][0] < word2[1][0]
        return word1[1][1] > word2[1][1]

    for k, v in enumerate(new_data):
        new_list = v.copy()
        # bubble sort
        for i in range(len(new_list)):
            for j in range(len(new_list) - i - 1):
                if compare_words(new_list[j], new_list[j + 1]):
                    new_list[j], new_list[j + 1] = new_list[j + 1], new_list[j]

    return new_data


def concatenate_by_line(provider: AnalysisProvider, data: list):
    lines = []
    for line in data:
        string = ""
        offset = 0
        for word, (left, _, right, _), _ in line:
            word = word.strip().replace("\n", " ")
            word = re.sub(" +", " ", word)
            if offset == 0 or (
                left - offset <= provider.word_width_tolerance
                and right - offset <= provider.word_width_tolerance
            ):
                string += word + " "
                offset = right
            else:
                string += ";" + word + " "
                offset = right
        lines.append(string)

    return lines


def parse_categories(provider: AnalysisProvider, data: list):
    category = None

    analysis = []

    categories = AnalysisCategoryName.objects.all()

    for line in data:
        for c in categories:
            if (
                fuzz.partial_ratio(line.lower(), c.name.lower())
                > provider.category_similarity
            ):
                category = c
                break
        t = line.split(";")
        if len(t) == 4:
            analysis.append(str(category.pk) + ";" + line)
        elif len(t) == 3:
            analysis.append(str(category.pk) + ";" + ";".join(t[:-1]) + ";;" + t[-1])
        elif len(t) > 4:
            analysis.append(str(category.pk) + ";" + ";".join(t[:4]) + " ".join(t[4:]))

    final_data = pd.read_csv(
        io.StringIO("\n".join(analysis)), sep=";", names=COLUMN_NAMES
    )
    final_data = final_data.replace(r"^\s*$", "", regex=True)

    return final_data


def create_table(provider: AnalysisProvider, tables):
    def extract_min_max(value):
        for regex in provider.range_extraction_regex:
            match = re.search(regex["regex"], str(value).strip())
            if match:
                if isinstance(regex["min"], str):
                    min_value = match.group(regex["min"])
                else:
                    min_value = regex["min"]
                if isinstance(regex["max"], str):
                    max_value = match.group(regex["max"])
                else:
                    max_value = regex["max"]
                return min_value, max_value
        return np.nan, np.nan

    final_table = tables.copy()
    if final_table.empty:
        final_table[[MIN_VALUE_COLUMN, MAX_VALUE_COLUMN]] = np.nan
        return final_table

    # If the Measurement Unit column is bigger than 20 characters, move it to Refference Range
    final_table.loc[
        final_table[MEASURE_UNIT_COLUMN].str.len() > 20,
        [REF_RANGE_COLUMN, MEASURE_UNIT_COLUMN],
    ] = final_table.loc[
        final_table[MEASURE_UNIT_COLUMN].str.len() > 20,
        [MEASURE_UNIT_COLUMN, REF_RANGE_COLUMN],
    ].values

    final_table[[MIN_VALUE_COLUMN, MAX_VALUE_COLUMN]] = (
        final_table[REF_RANGE_COLUMN].apply(extract_min_max).tolist()
    )

    final_table[RESULT_COLUMN] = final_table[RESULT_COLUMN].astype(str)
    final_table["length"] = final_table[RESULT_COLUMN].str.len()
    final_table = final_table[final_table["length"] < 20]
    final_table = final_table[final_table["length"] != 0]

    final_table[NAME_COLUMN] = final_table[NAME_COLUMN].astype(str)
    final_table["length"] = final_table[NAME_COLUMN].str.len()
    final_table = final_table[final_table["length"] < 70]
    final_table = final_table[final_table["length"] != 0]

    final_table[IN_RANGE_COLUMN] = final_table.apply(
        lambda x: np.nan
        if not (
            re.match(r"^\d+[\.,]?\d*$", x[RESULT_COLUMN])
            and not pd.isna(x[MIN_VALUE_COLUMN])
            and not pd.isna(x[MAX_VALUE_COLUMN])
        )
        else float(x[RESULT_COLUMN]) >= float(x[MIN_VALUE_COLUMN])
        and float(x[RESULT_COLUMN]) <= float(x[MAX_VALUE_COLUMN]),
        axis=1,
    )

    for key, value in provider.replace_results.items():
        final_table[RESULT_COLUMN] = final_table[RESULT_COLUMN].str.replace(
            key, str(value)
        )

    final_table = final_table.drop(columns=["length"])
    return final_table
