/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // ===== Obsidian Protocol — Surface Hierarchy =====
        surface: {
          DEFAULT: '#121318',
          dim: '#121318',
          bright: '#38393e',
          'container-lowest': '#0d0e13',
          'container-low': '#1a1b20',
          container: '#1e1f25',
          'container-high': '#292a2f',
          'container-highest': '#34343a',
          variant: '#34343a',
          tint: '#bbc3ff',
        },
        // ===== Landing Page HTML Colors =====
        lp: {
          primary: '#002B5B',
          secondary: '#2563EB',
          tertiary: '#00D1FF',
          surface: '#FFFFFF',
          'surface-container': '#F8FAFC',
          'surface-container-high': '#F1F5F9',
          'on-surface': '#0F172A',
          'on-surface-variant': '#475569',
          outline: '#E2E8F0',
          error: '#DC2626',
          success: '#059669',
        },
        // ===== Primary — Electric Blue =====
        primary: {
          DEFAULT: '#dfe1ff',
          container: '#bbc3ff',
          fixed: '#dee0ff',
          'fixed-dim': '#bbc3ff',
        },
        'on-primary': {
          DEFAULT: '#242c5e',
          container: '#474f83',
          fixed: '#0d1648',
          'fixed-variant': '#3b4376',
        },
        // ===== Secondary — Soft Violet =====
        secondary: {
          DEFAULT: '#d1bcff',
          container: '#503f79',
          fixed: '#eaddff',
          'fixed-dim': '#d1bcff',
        },
        'on-secondary': {
          DEFAULT: '#37265e',
          container: '#c2aef0',
          fixed: '#220f48',
          'fixed-variant': '#4e3d76',
        },
        // ===== Tertiary — Cyan Neon =====
        tertiary: {
          DEFAULT: '#66f7ff',
          container: '#00dce5',
          fixed: '#63f7ff',
          'fixed-dim': '#00dce5',
        },
        'on-tertiary': {
          DEFAULT: '#003739',
          container: '#005c60',
          fixed: '#002021',
          'fixed-variant': '#004f53',
        },
        // ===== On-Surface =====
        'on-surface': {
          DEFAULT: '#e3e1e9',
          variant: '#c6c5d0',
        },
        'on-background': '#e3e1e9',
        // ===== Error =====
        error: {
          DEFAULT: '#ffb4ab',
          container: '#93000a',
        },
        'on-error': {
          DEFAULT: '#690005',
          container: '#ffdad6',
        },
        // ===== Outline =====
        outline: {
          DEFAULT: '#90909a',
          variant: '#46464f',
        },
        // ===== Inverse =====
        inverse: {
          surface: '#e3e1e9',
          'on-surface': '#2f3036',
          primary: '#525b90',
        },
        // ===== Legacy compat =====
        success: '#10B981',
        warning: '#F59E0B',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        headline: ['"Space Grotesk"', 'sans-serif'],
        body: ['"Inter"', 'sans-serif'],
        label: ['"Manrope"', 'sans-serif'],
      },
      borderRadius: {
        obsidian: '8px',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 10s linear infinite',
        'spin-slower': 'spin 15s linear infinite reverse',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 12px rgba(0, 220, 229, 0.15)' },
          '100%': { boxShadow: '0 0 24px rgba(0, 220, 229, 0.3)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        },
      },
      boxShadow: {
        'ambient': '0 8px 40px rgba(52, 52, 58, 0.06)',
        'ambient-lg': '0 16px 60px rgba(52, 52, 58, 0.1)',
        'intelligence': '0 0 24px rgba(0, 220, 229, 0.15)',
        'primary-glow': '0 0 20px rgba(187, 195, 255, 0.2)',
      },
      backdropBlur: {
        'glass': '24px',
      },
    },
  },
  plugins: [],
}
