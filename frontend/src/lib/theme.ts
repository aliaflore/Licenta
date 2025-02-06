
import type { CustomThemeConfig } from '@skeletonlabs/tw-plugin';

export const myCustomTheme: CustomThemeConfig = {
    name: 'my-custom-theme',
    properties: {
		// =~= Theme Properties =~=
		"--theme-font-family-base": `system-ui`,
		"--theme-font-family-heading": `system-ui`,
		"--theme-font-color-base": "0 0 0",
		"--theme-font-color-dark": "255 255 255",
		"--theme-rounded-base": "9999px",
		"--theme-rounded-container": "8px",
		"--theme-border-base": "1px",
		// =~= Theme On-X Colors =~=
		"--on-primary": "0 0 0",
		"--on-secondary": "0 0 0",
		"--on-tertiary": "255 255 255",
		"--on-success": "0 0 0",
		"--on-warning": "0 0 0",
		"--on-error": "255 255 255",
		"--on-surface": "0 0 0",
		// =~= Theme Colors  =~=
		// primary | #b56357 
		"--color-primary-50": "244 232 230", // #f4e8e6
		"--color-primary-100": "240 224 221", // #f0e0dd
		"--color-primary-200": "237 216 213", // #edd8d5
		"--color-primary-300": "225 193 188", // #e1c1bc
		"--color-primary-400": "203 146 137", // #cb9289
		"--color-primary-500": "181 99 87", // #b56357
		"--color-primary-600": "163 89 78", // #a3594e
		"--color-primary-700": "136 74 65", // #884a41
		"--color-primary-800": "109 59 52", // #6d3b34
		"--color-primary-900": "89 49 43", // #59312b
		// secondary | #b4d8c0 
		"--color-secondary-50": "244 249 246", // #f4f9f6
		"--color-secondary-100": "240 247 242", // #f0f7f2
		"--color-secondary-200": "236 245 239", // #ecf5ef
		"--color-secondary-300": "225 239 230", // #e1efe6
		"--color-secondary-400": "203 228 211", // #cbe4d3
		"--color-secondary-500": "180 216 192", // #b4d8c0
		"--color-secondary-600": "162 194 173", // #a2c2ad
		"--color-secondary-700": "135 162 144", // #87a290
		"--color-secondary-800": "108 130 115", // #6c8273
		"--color-secondary-900": "88 106 94", // #586a5e
		// tertiary | #a7b3a5 
		"--color-tertiary-50": "242 244 242", // #f2f4f2
		"--color-tertiary-100": "237 240 237", // #edf0ed
		"--color-tertiary-200": "233 236 233", // #e9ece9
		"--color-tertiary-300": "220 225 219", // #dce1db
		"--color-tertiary-400": "193 202 192", // #c1cac0
		"--color-tertiary-500": "167 179 165", // #a7b3a5
		"--color-tertiary-600": "150 161 149", // #96a195
		"--color-tertiary-700": "125 134 124", // #7d867c
		"--color-tertiary-800": "100 107 99", // #646b63
		"--color-tertiary-900": "82 88 81", // #525851
		// success | #4273e6 
		"--color-success-50": "227 234 251", // #e3eafb
		"--color-success-100": "217 227 250", // #d9e3fa
		"--color-success-200": "208 220 249", // #d0dcf9
		"--color-success-300": "179 199 245", // #b3c7f5
		"--color-success-400": "123 157 238", // #7b9dee
		"--color-success-500": "66 115 230", // #4273e6
		"--color-success-600": "59 104 207", // #3b68cf
		"--color-success-700": "50 86 173", // #3256ad
		"--color-success-800": "40 69 138", // #28458a
		"--color-success-900": "32 56 113", // #203871
		// warning | #ed2665 
		"--color-warning-50": "252 222 232", // #fcdee8
		"--color-warning-100": "251 212 224", // #fbd4e0
		"--color-warning-200": "251 201 217", // #fbc9d9
		"--color-warning-300": "248 168 193", // #f8a8c1
		"--color-warning-400": "242 103 147", // #f26793
		"--color-warning-500": "237 38 101", // #ed2665
		"--color-warning-600": "213 34 91", // #d5225b
		"--color-warning-700": "178 29 76", // #b21d4c
		"--color-warning-800": "142 23 61", // #8e173d
		"--color-warning-900": "116 19 49", // #741331
		// error | #843fc5 
		"--color-error-50": "237 226 246", // #ede2f6
		"--color-error-100": "230 217 243", // #e6d9f3
		"--color-error-200": "224 207 241", // #e0cff1
		"--color-error-300": "206 178 232", // #ceb2e8
		"--color-error-400": "169 121 214", // #a979d6
		"--color-error-500": "132 63 197", // #843fc5
		"--color-error-600": "119 57 177", // #7739b1
		"--color-error-700": "99 47 148", // #632f94
		"--color-error-800": "79 38 118", // #4f2676
		"--color-error-900": "65 31 97", // #411f61
		// surface | #eae3ea 
		"--color-surface-50": "252 251 252", // #fcfbfc
		"--color-surface-100": "251 249 251", // #fbf9fb
		"--color-surface-200": "250 248 250", // #faf8fa
		"--color-surface-300": "247 244 247", // #f7f4f7
		"--color-surface-400": "240 235 240", // #f0ebf0
		"--color-surface-500": "234 227 234", // #eae3ea
		"--color-surface-600": "211 204 211", // #d3ccd3
		"--color-surface-700": "176 170 176", // #b0aab0
		"--color-surface-800": "140 136 140", // #8c888c
		"--color-surface-900": "115 111 115", // #736f73
		
	}
}