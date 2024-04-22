/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    fontSize:{
      xs:'0.65rem',
    },
    
    extend: {
      maxHeight:{
        fitted: "calc(100vh - 48px)",
      },
    },
  },
  plugins: [],
}

