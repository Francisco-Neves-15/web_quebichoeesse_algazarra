import { type Config } from "tailwindcss"

const config: Config = {
  content: [
    "./src/app/**/*.{ts,tsx}",
    "./src/components/**/*.{ts,tsx}",
    "./src/contexts/**/*.{ts,tsx}",
    "./src/utils/**/*.{ts,tsx}",
  ],
  darkMode: "class",
  plugins: [],
}

export default config
