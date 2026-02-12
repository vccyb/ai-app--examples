/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 赛博修仙主题色彩
        'cyber-black': '#0a0a0a',
        'cyber-purple': '#1a0a2e',
        'neon-pink': '#ff006e',
        'neon-cyan': '#00f5ff',
        'neon-gold': '#ffd700',
      },
      fontFamily: {
        'cyber': ['"Courier New"', 'monospace'], // 等宽字体用于数据显示
      },
      boxShadow: {
        'neon-pink': '0 0 10px #ff006e, 0 0 20px #ff006e',
        'neon-cyan': '0 0 10px #00f5ff, 0 0 20px #00f5ff',
        'neon-gold': '0 0 10px #ffd700, 0 0 20px #ffd700',
      },
    },
  },
  plugins: [],
}
