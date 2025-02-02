export interface User {
    pk:           number;
    url:          string;
    email:        string;
    username:     string;
    first_name:   string;
    last_name:    string;
    is_staff:     boolean;
    is_doctor:    boolean;
    is_superuser: boolean;
    full_name:    string;
    date_joined:  Date;
    is_paying:    boolean;
}

export interface Error {
	error: string;
}

export interface UserResult {
	user: User;
}

export interface AnalysisProvider {
	pk: number;
	url: string;
	name: string;
	crops_words: CropsWords;
	crops_pixels: CropsPixels;
	crop_similarity: number;
	line_height_tolerance: number;
	word_width_tolerance: number;
	line_continuation_difference_width: number;
	category_similarity: number;
	range_extraction_regex: RangeExtractionRegex[];
	ignored_words: string[];
	space_pixels: number;
	replace_results: ReplaceResults;
	analysis_list: string;
	analysis_providedlang: string;
	analysis_list_skip_first_row: boolean;
	analysis_list_skip_first_table: boolean;
	analysis_columns: number[];
}

export interface CropsPixels {
	left: number;
}

export interface CropsWords {
	top: string[];
	bottom: string[];
}

export interface RangeExtractionRegex {
	regex: string;
	min: number | string;
	max: string;
}

export interface ReplaceResults {}

export interface PaginatedResult<T> {
	results: T[];
	count: number;
	next: string;
	previous: string;
}

export type AnalysisProviderResult = AnalysisProvider[];

export interface RadiographyPDF {
	pk: number;
	url: string;
	file: string;
	provider: SimpleAnalysisProvider;
	user: User;
	created: Date;
	taken_on: Date;
	doctor_notes: string;
	modified: Date;
}

export interface SimpleAnalysisProvider {
	pk: number;
	name: string;
}

export interface AnalysisPDF {
	pk: number;
	url: string;
	file: string;
	provider: SimpleAnalysisProvider;
	user: User;
	created: Date;
	taken_on: null;
	doctor_notes: string;
	suggestion: string;
	analysis?: string;
	analysis_id?: number;
	modified: Date;
}

export interface Analysis {
	url: string;
	source: AnalysisPDF;
	created: Date;
	results: AnalysisResult[];
	notes: string;
}

export interface AnalysisResult {
	url: string;
	pk: number;
	name: string;
	category: AnalysisCategory;
	result: string;
	measurement_unit: string;
	refference_range: string;
	range_min: null | string;
	range_max: null | string;
	in_range: boolean | null;
	suggestion: string;
    approve_ai_suggestion: boolean;
	doctor_note: string;
	created: Date;
	modified: Date;
}

export interface AnalysisCategory {
	pk: number;
	name: string;
	related_names: string[];
}

export type AnalysisPDFResult = PaginatedResult<AnalysisPDF>;

export interface RadiographyPDF {
	pk: number;
	url: string;
	file: string;
	provider: SimpleAnalysisProvider;
	user: User;
	created: Date;
	taken_on: Date;
	doctor_notes: string;
	modified: Date;
}

export type RadiographyPDFResult = PaginatedResult<RadiographyPDF>;

export type HistoryAnalysisResult = AnalysisResult & { date?: string };

export interface HistoryData {
    name:     string;
    category: SimpleAnalysisCategory;
    data:     HistoryAnalysisResult[];
}

export interface SimpleAnalysisCategory {
    pk:   number;
    name: string;
}

export type HistoryDataResult = HistoryData[];

export interface PatientInvite {
    url:         string;
    pk:          number;
    patient:     User;
    doctor:      User;
    expires:     Date;
    accepted:    boolean;
    accepted_on: Date;
    created:     Date;
    modified:    Date;
}

export type PatientInviteResult = PaginatedResult<PatientInvite>;