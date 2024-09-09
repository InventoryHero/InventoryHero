import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import autoImportGlobals from "./.eslintrc-auto-import.json" assert {type: 'json'}

export default [

    {
        files: ["**/*.{js,mjs,cjs,ts,vue}"]
    },
    {
        languageOptions: {
            globals: {
                ...globals.browser,
                ...autoImportGlobals["globals"]
            },
        }
    },
    pluginJs.configs.recommended,
    ...tseslint.configs.recommended,
    ...pluginVue.configs["flat/essential"],
    {
        rules: {
            'vue/multi-word-component-names': 'off',
            'vue/valid-v-slot': 'off',
            'vue/no-v-text-v-html-on-component': 'off'
        }
    },
    {
        files: ["**/*.vue"],
        languageOptions: {
            parserOptions: {
                parser: tseslint.parser
            }
        }
    },
    {
        ignores: ['dev-dist/*', 'src/vue-virtual-scroller.d.ts']
    }
];