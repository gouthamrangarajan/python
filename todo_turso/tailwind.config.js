/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["*.py", "assets/*.js"],
  theme: {
    extend: {
      animation: {
        list: 'list 0.3s var(--ease-1)',
        opacity: 'opacity 0.3s var(--ease-1)',
        login: 'login 2s var(--ease-spring-3)'
      },
      keyframes: {
        login: {
          from: {
            opacity: 0,
            transform: 'translateY(-5rem)'
          },
          to: {
            opacity: 1,
            transform: 'translateY(0)'
          }
        },
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

