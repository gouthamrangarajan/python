/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["*.py"],
  theme: {
    extend: {
      animation: {
        list: 'list 0.3s ease-in-out',
        opacity: 'opacity 0.3s ease-in-out'
      },
      keyframes: {
        list: {
          from: {
            opacity: 0,
            transform: 'translateY(-5px)'
          },
          to: {
            opacity: 1,
            transform: 'translateY(0)'
          }
        },
        opacity: {
          from: {
            opacity: 0
          },
          to: {
            opacity: 1
          }
        },

      }
    },
  },
  plugins: [],
}

