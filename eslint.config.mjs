import js from "@eslint/js";
import eslintPluginUnicorn from 'eslint-plugin-unicorn'
import globals from "globals"

export default [
  eslintPluginUnicorn.configs.all,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        langs: true,
        $: false
      }
    },
    rules: {
      ...js.configs.recommended.rules,
      "unicorn/no-keyword-prefix": 0,
      "unicorn/prefer-query-selector": 0
    },
  }
]
