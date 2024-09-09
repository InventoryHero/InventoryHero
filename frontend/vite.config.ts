// noinspection ES6PreferShortImport
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'
//@ts-expect-error
import {fileURLToPath, URL} from "node:url";
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import {i18n} from './src/lang';
import vuetify from "vite-plugin-vuetify";

export default defineConfig({
  build: {
    target: "esnext",
    sourcemap: false
  },
  plugins: [
    vue(),
    vuetify(),
    VitePWA({
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
      manifest: {
        name: "InventoryHero",
        short_name: "IH",
        description: i18n.global.t('description'),
        theme_color: "#64B5F6",
        display: "standalone",
        icons: [
          {
            "src": "android-chrome-192x192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any"
          },
          {
            "src": "android-chrome-maskable-192x192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "maskable"
          },
          {
            "src": "android-chrome-512x512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any"
          },
          {
            "src": "android-chrome-maskable-512x512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable"
          }
        ]
      },
      workbox: {
        clientsClaim: true,
        skipWaiting: true,
        maximumFileSizeToCacheInBytes: 8000000
      },
      devOptions: {
        enabled: true
      }
    }),
    AutoImport({
      include: [
        /\.[tj]sx?$/, // .ts, .tsx, .js, .jsx
        /\.vue$/,
        /\.vue\?vue/, // .vue
      ],
      imports: [
        'vue',
        'vue-router',
        {
          'vue-i18n':[
              'useI18n'
          ]
        }
      ]
    }),
    Components({
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    }
  },
  server:{
    port: 3000,
    proxy: {
      "/api/v1": {
        target: 'http://127.0.0.1:5000/'
      },
      "/socket.io": {
        target: 'ws://localhost:5000',
        ws: true,
      }
    }
  }
})

