import requests
import camelot
import pandas as pd
import numpy as np
from licenta.models import AnalysisProvider, Translation
from deep_translator import GoogleTranslator
from django.conf import settings
import tempfile
import logging
from thefuzz import fuzz


logger = logging.getLogger(__name__)


class PDFCategoryImporter:
    def __init__(self, provider: AnalysisProvider):
        self.provider = provider
        self.imported_language = self.provider.analysis_providedlang
        self.data: dict[str, list[str]] = {self.imported_language: []}

    def provide(self):
        pdf = requests.get(self.provider.analysis_list)
        with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
            f.write(pdf.content)
            f.seek(0)
            tables = camelot.read_pdf(f.name, pages="all")
        if self.provider.analysis_list_skip_first_table:
            data = pd.concat([table.df for table in tables[1:]])
        else:
            data = pd.concat([table.df for table in tables])
        if self.provider.analysis_list_skip_first_row:
            data = data.iloc[1:]

        data = pd.concat([data.iloc[:, column] for column in self.provider.analysis_columns], axis=1)
        data.replace('', np.nan, inplace=True)
        data.dropna(inplace=True)
        data.drop_duplicates(inplace=True)
        data.reset_index(drop=True, inplace=True)

        print(data)

        self.data = {
            self.provider.analysis_providedlang: list(data.iloc[:, 0].values)
        }
        return self.data


class TranslatedCategoryImport:
    def __init__(self, base_import: PDFCategoryImporter, languages: list[str] = settings.ANALYSIS_TRANSLATE_LANGUAGES):
        self.base_import = base_import
        self.languages = languages
        self.data: dict[str, list[str]] = {lang: [] for lang in languages}

    def provide(self):
        self.translate()
        return self.data

    def translate(self):
        self.data[self.base_import.imported_language] = self.base_import.data[self.base_import.imported_language]
        for lang in self.languages:
            not_translated = []
            not_translated_idx = []
            if lang != self.base_import.imported_language:
                self.data[lang] = [""] * len(self.base_import.data[self.base_import.imported_language])
                for idx, name in enumerate(self.base_import.data[self.base_import.imported_language]):
                    already_translated = Translation.objects.filter(
                        original_text=name,
                        source_language=self.base_import.imported_language,
                    ).first()
                    if already_translated:
                        self.data[lang][idx] = already_translated.translated_text
                    else:
                        not_translated.append(name)
                        not_translated_idx.append(idx)
                translator = GoogleTranslator(source=self.base_import.imported_language, target=lang)
                for idx, original in zip(not_translated_idx, not_translated):
                    translated = translator.translate(original)
                    self.data[lang][idx] = translated
                    Translation.objects.create(
                        original_text=original,
                        source_language=self.base_import.imported_language,
                        translated_text=translated,
                        target_language=lang
                    )
                    logger.info("Translation received", extra={
                        "original": original,
                        "translated": translated,
                        "source": self.base_import.imported_language,
                        "target": lang
                    })



class CategoryImportMatcher:
    def __init__(self, translated: list[TranslatedCategoryImport]):
        self.translated = translated
        self.matched: dict[str, list[str]] = {lang: [] for lang in self.translated[0].languages}

        self.verify()

    def verify(self):
        assert len(self.translated) >= 1

        languages = list(map(lambda x: x.data.keys(), self.translated))
        assert all([lang == languages[0] for lang in languages])

        assert all([len(t.data) == len(self.translated[0].data) for t in self.translated])

    def match(self):
        self.verify()
        matched: list[list[tuple[str, str]]] = []

        for t in self.translated:
            m1 = []
            for language in t.data:
                for idx, name in enumerate(t.data[language]):
                    if len(m1) <= idx:
                        m1.append([])
                    m1[idx].append((language, name))
            matched.extend(m1)

        finished_matching = []

        continue_grouping = True
        while continue_grouping:
            new_matched = []
            continue_grouping = False
            has_matched = [False] * len(matched)
            for idx1, group1 in enumerate(matched):
                if idx1 % 100 == 0:
                    logger.debug("Still Matching", extra={
                        "idx": idx1,
                        "total": len(matched)
                    })
                if has_matched[idx1]:
                    continue
                for idx2, group2 in enumerate(matched):
                    if group1 == group2 or has_matched[idx1] or has_matched[idx2]:
                        continue
                    combine = False
                    for word1 in group1:
                        for word2 in group2:
                            # Skip if the words are in different languages
                            if word1[0] != word2[0]:
                                continue
                            if len(word1[1].split(',')) != len(word2[1].split(',')):
                                continue
                            combine = all(
                                [fuzz.partial_ratio(split1, split2) > 90 for split1, split2 in zip(word1[1].split(','), word2[1].split(','))]
                            )
                            if combine:
                                break
                    if combine:
                        continue_grouping = True
                        has_matched[idx1] = True
                        has_matched[idx2] = True
                        new_matched.append(group1 + group2)
                        break
            for idx, group in enumerate(matched):
                if not has_matched[idx]:
                    finished_matching.append(group)
            matched = new_matched

            logger.debug("Finished matching one time", extra={
                "finished_matching": len(finished_matching),
                "matched": len(matched)
            })

        return finished_matching