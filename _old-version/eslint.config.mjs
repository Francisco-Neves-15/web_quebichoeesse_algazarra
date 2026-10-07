import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Não configurado corretamente
  // {
  //   rules: {
  //     "camelcase": ["error", { "properties": "always" }],
  //     "@typescript-eslint/naming-convention": [
  //       "error",
  //       {
  //         "selector": "variable",
  //         "modifiers": ["const"],
  //         "format": ["UPPER_CASE"]
  //       },
  //       {
  //         "selector": "variable",
  //         "modifiers": [],
  //         "format": ["camelCase"]
  //       }
  //     ]
  //   }
  // },
  {
    rules: {
      "prefer-const": "off",
      "@typescript-eslint/no-explicit-any": "warn"
    }
  },
  {
    files: ["src/**/*.jsx"],
    rules: {
      "no-restricted-syntax": [
        "error",
        {
          "selector": "Program",
          "message": ".jsx files are not allowed in the src directory. Use .tsx, .ts, or .js files."
        }
      ]
    }
  },
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
  ]),
]);

export default eslintConfig;
