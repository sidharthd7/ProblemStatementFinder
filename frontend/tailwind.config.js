/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily:{
        sans: ['Urbanist', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors:{
        blue: {
          500: '#01AFF6',
          600: '#00A3F5',
          700: '#008FF5',
        },
      },
    },
  },
  plugins: [],
}

