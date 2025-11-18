/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'vader-red': '#DC143C',
        'vader-black': '#0A0A0A',
        'vader-gray': '#1A1A1A',
        'empire-silver': '#C0C0C0',
      },
      fontFamily: {
        'star-wars': ['Orbitron', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
