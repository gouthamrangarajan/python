/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["*.py", "assets/*.js"],
  theme: {
    extend: {
      keyframes: {
        'scale-y': {
          from: { opacity: 0, transform: "scaleY(0)" },
          to: { opacity: 1, transform: "scaleY(1)" }
        }
      },
      animation: {
        'scale-y': "scale-y 1s var(--ease-spring-3)",
        'bounce-1': "bounce 0.5s infinite",
        'bounce-2': "bounce 1s infinite",
        'bounce-3': "bounce 1.5s infinite",
      },
      transitionTimingFunction: {
        'in-out-1': "var(--ease-in-out-1)",
        'spring-3': "var(--ease-spring-3)"
      }
    },
  },
  plugins: [require('tailwind-scrollbar'),
  ],
}

