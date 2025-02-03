
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
		"--on-tertiary": "0 0 0",
		"--on-success": "0 0 0",
		"--on-warning": "0 0 0",
		"--on-error": "0 0 0",
		"--on-surface": "0 0 0",
		// =~= Theme Colors  =~=
		// primary | #5bbcbb 
		"--color-primary-50": "230 245 245", // #e6f5f5
		"--color-primary-100": "222 242 241", // #def2f1
		"--color-primary-200": "214 238 238", // #d6eeee
		"--color-primary-300": "189 228 228", // #bde4e4
		"--color-primary-400": "140 208 207", // #8cd0cf
		"--color-primary-500": "91 188 187", // #5bbcbb
		"--color-primary-600": "82 169 168", // #52a9a8
		"--color-primary-700": "68 141 140", // #448d8c
		"--color-primary-800": "55 113 112", // #377170
		"--color-primary-900": "45 92 92", // #2d5c5c
		// secondary | #c2552e 
		"--color-secondary-50": "246 230 224", // #f6e6e0
		"--color-secondary-100": "243 221 213", // #f3ddd5
		"--color-secondary-200": "240 213 203", // #f0d5cb
		"--color-secondary-300": "231 187 171", // #e7bbab
		"--color-secondary-400": "212 136 109", // #d4886d
		"--color-secondary-500": "194 85 46", // #c2552e
		"--color-secondary-600": "175 77 41", // #af4d29
		"--color-secondary-700": "146 64 35", // #924023
		"--color-secondary-800": "116 51 28", // #74331c
		"--color-secondary-900": "95 42 23", // #5f2a17
		// tertiary | #e6cd9c 
		"--color-tertiary-50": "251 248 240", // #fbf8f0
		"--color-tertiary-100": "250 245 235", // #faf5eb
		"--color-tertiary-200": "249 243 230", // #f9f3e6
		"--color-tertiary-300": "245 235 215", // #f5ebd7
		"--color-tertiary-400": "238 220 186", // #eedcba
		"--color-tertiary-500": "230 205 156", // #e6cd9c
		"--color-tertiary-600": "207 185 140", // #cfb98c
		"--color-tertiary-700": "173 154 117", // #ad9a75
		"--color-tertiary-800": "138 123 94", // #8a7b5e
		"--color-tertiary-900": "113 100 76", // #71644c
		// success | #5d808a 
		"--color-success-50": "231 236 237", // #e7eced
		"--color-success-100": "223 230 232", // #dfe6e8
		"--color-success-200": "215 223 226", // #d7dfe2
		"--color-success-300": "190 204 208", // #beccd0
		"--color-success-400": "142 166 173", // #8ea6ad
		"--color-success-500": "93 128 138", // #5d808a
		"--color-success-600": "84 115 124", // #54737c
		"--color-success-700": "70 96 104", // #466068
		"--color-success-800": "56 77 83", // #384d53
		"--color-success-900": "46 63 68", // #2e3f44
		// warning | #827299 
		"--color-warning-50": "236 234 240", // #eceaf0
		"--color-warning-100": "230 227 235", // #e6e3eb
		"--color-warning-200": "224 220 230", // #e0dce6
		"--color-warning-300": "205 199 214", // #cdc7d6
		"--color-warning-400": "168 156 184", // #a89cb8
		"--color-warning-500": "130 114 153", // #827299
		"--color-warning-600": "117 103 138", // #75678a
		"--color-warning-700": "98 86 115", // #625673
		"--color-warning-800": "78 68 92", // #4e445c
		"--color-warning-900": "64 56 75", // #40384b
		// error | #b17080 
		"--color-error-50": "243 234 236", // #f3eaec
		"--color-error-100": "239 226 230", // #efe2e6
		"--color-error-200": "236 219 223", // #ecdbdf
		"--color-error-300": "224 198 204", // #e0c6cc
		"--color-error-400": "200 155 166", // #c89ba6
		"--color-error-500": "177 112 128", // #b17080
		"--color-error-600": "159 101 115", // #9f6573
		"--color-error-700": "133 84 96", // #855460
		"--color-error-800": "106 67 77", // #6a434d
		"--color-error-900": "87 55 63", // #57373f
		// surface | #deabfc 
		"--color-surface-50": "250 242 255", // #faf2ff
		"--color-surface-100": "248 238 254", // #f8eefe
		"--color-surface-200": "247 234 254", // #f7eafe
		"--color-surface-300": "242 221 254", // #f2ddfe
		"--color-surface-400": "232 196 253", // #e8c4fd
		"--color-surface-500": "222 171 252", // #deabfc
		"--color-surface-600": "200 154 227", // #c89ae3
		"--color-surface-700": "167 128 189", // #a780bd
		"--color-surface-800": "133 103 151", // #856797
		"--color-surface-900": "109 84 123", // #6d547b
		
	}
}