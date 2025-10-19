// eslint.config.mjs

import js from "@eslint/js";
import html from "eslint-plugin-html";
import globals from "globals";
import { defineConfig } from "eslint/config";

export default defineConfig([
  // Configuração base para JS
  {
    files: ["**/*.{js,mjs,cjs}"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: globals.browser
    },
    plugins: { html },
    extends: [js.configs.recommended]
  },

  // Configuração para HTML e Jinja2 templates
  {
    files: ["**/*.{html,jinja,jinja2}"],
    plugins: { html },
    settings: {
      "html/html-extensions": [".html", ".jinja", ".jinja2"]
    }
  }
]);
