export interface User {
    url: string;
    username: string;
    email: string;
    is_staff: boolean;
    id: number;
};

export interface Error {
    error: string;
};

export interface UserResult {
    user: User;
}

export interface AnalysisProvider {
    pk:                                 number;
    url:                                string;
    name:                               string;
    crops_words:                        CropsWords;
    crops_pixels:                       CropsPixels;
    crop_similarity:                    number;
    line_height_tolerance:              number;
    word_width_tolerance:               number;
    line_continuation_difference_width: number;
    category_similarity:                number;
    range_extraction_regex:             RangeExtractionRegex[];
    ignored_words:                      string[];
    space_pixels:                       number;
    replace_results:                    ReplaceResults;
    analysis_list:                      string;
    analysis_providedlang:              string;
    analysis_list_skip_first_row:       boolean;
    analysis_list_skip_first_table:     boolean;
    analysis_columns:                   number[];
}

export interface CropsPixels {
    left: number;
}

export interface CropsWords {
    top:    string[];
    bottom: string[];
}

export interface RangeExtractionRegex {
    regex: string;
    min:   number | string;
    max:   string;
}

export interface ReplaceResults {
}

export interface PaginatedResult<T> {
    results: T[];
    count:    number;
    next:     string;
    previous: string;
}

export type AnalysisProviderResult = AnalysisProvider[];

export interface RadiographyPDF {
    pk:           number;
    url:          string;
    file:         string;
    provider:     SimpleAnalysisProvider;
    user:         User;
    created:      Date;
    taken_on:     Date;
    doctor_notes: string;
    modified:     Date;
}

export interface SimpleAnalysisProvider {
    pk:   number;
    name: string;
}

export interface AnalysisPDF {
    pk:           number;
    url:          string;
    file:         string;
    provider:     SimpleAnalysisProvider;
    user:         User;
    created:      Date;
    taken_on:     null;
    doctor_notes: string;
    suggestion:   string;
    analysis:     string;
    modified:     Date;
}

export type AnalysisPDFResult = PaginatedResult<AnalysisPDF>;

