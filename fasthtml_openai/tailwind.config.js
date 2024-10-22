/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["*.py", "assets/*.js"],
  theme: {
    extend: {
      keyframes: {
        'scale-y': {
          from: { opacity: 0, transform: "scaleY(0)" },
          to: { opacity: 1, transform: "scaleY(1)" }
        },
        'slide-right': {
          from: { opacity: 0, transform: "translateX(-100%)" },
          to: { opacity: 1, transform: "translateX(0)" }
        },
        'slide-right-opp': {
          from: { opacity: 1, transform: "translateX(0)" },
          to: { opacity: 0, transform: "translateX(-100%)" }
        }
      },
      animation: {
        'scale-y': "scale-y 1s var(--ease-spring-3)",
        'bounce-1': "bounce 0.5s infinite",
        'bounce-2': "bounce 1s infinite",
        'bounce-3': "bounce 1.5s infinite",
        "slide-right": "slide-right 0.3s var(--ease-in-out-1)",
        "slide-right-opp": "slide-right-opp 0.3s var(--ease-in-out-1)"
      }
    },
  },
  plugins: [require('tailwind-scrollbar'),
  ],
}

