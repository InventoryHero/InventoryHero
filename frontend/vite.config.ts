// noinspection ES6PreferShortImport
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'
import VueRouter from 'unplugin-vue-router/vite'
import { VueRouterAutoImports } from 'unplugin-vue-router'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import { i18n } from './src/plugins/i18n'
import vuetify from 'vite-plugin-vuetify'
import mkcert from 'vite-plugin-mkcert'
import Layouts from 'vite-plugin-vue-layouts-next'
import Unfonts from 'unplugin-fonts/vite'

//@ts-expect-error node url cannot be found, but it is there
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  build: {
    target: 'esnext',
    sourcemap: false
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/scss/transitions.scss";`
      }
    }
  },
  plugins: [
    Unfonts({}),
    mkcert(),
    VueRouter({}),
    vue(),
    Layouts({
      layoutsDirs: 'src/layouts',
      pagesDirs: 'src/pages',
      defaultLayout: 'default'
    }),
    vuetify(),
    VitePWA({
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
      manifest: {
        name: 'InventoryHero',
        short_name: 'IH',
        description: i18n.global.t('description'),
        theme_color: '#64B5F6',
        display: 'standalone',
        icons: [
          {
            src: 'android-chrome-192x192.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'any'
          },
          {
            src: 'android-chrome-maskable-192x192.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'maskable'
          },
          {
            src: 'android-chrome-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any'
          },
          {
            src: 'android-chrome-maskable-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }
        ]
      },
      workbox: {
        navigateFallbackDenylist: [/^\/api\//],
        runtimeCaching: [
          {
            urlPattern: /^\/api\//,
            handler: 'NetworkOnly'
          }
        ]
      },
      devOptions: {
        enabled: true
      }
    }),
    AutoImport({
      eslintrc: {
        enabled: true
      },
      include: [
        /\.[tj]sx?$/, // .ts, .tsx, .js, .jsx
        /\.vue$/,
        /\.vue\?vue/ // .vue
      ],
      dirs: ['./src/composables'],
      imports: [
        'vue',
        VueRouterAutoImports,
        'pinia',
        {
          'vue-i18n': ['useI18n'],
          vuetify: ['useDisplay']
        }
      ]
    }),
    Components({})
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    https: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000/',
        ws: true,
        changeOrigin: true
      } /*,
      '/socket.io': {
        target: 'ws://localhost:5000',
        ws: true
      }*/
    }
  }
})
