/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          blue: '#1d4ed8',
          indigo: '#4338ca',
          sky: '#38bdf8',
        },
      },
    },
  },
  plugins: [],
};