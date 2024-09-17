import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      colors: {
        eco: {
          100: "#eafff3",
          200: "#d4ffe6",
          300: "#bfffda",
          400: "#a9ffcd",
          500: "#94ffc1",
          600: "#76cc9a",
          700: "#599974",  
          800: "#3b664d",
          900: "#1e3327",

        },
        pinkish: {
          100: "#fff3f3",
          200: "#ffe7e7",
          300: "#ffdada",
          400: "#ffcece",
          500: "#ffc2c2",
          600: "#cc9b9b",
          700: "#997474",
          800: "#664e4e",
          900: "#332727"
},
      },
    },
  },
  plugins: [],
};
export default config;
