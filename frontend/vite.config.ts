// noinspection ES6PreferShortImport

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'
import {fileURLToPath, URL} from "node:url";
import Components from 'unplugin-vue-components/vite'
import {i18n} from './src/lang';
import basicSsl from '@vitejs/plugin-basic-ssl'
import vuetify from "vite-plugin-vuetify";

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    target: "esnext"
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
      devOptions: {
        enabled: true
      }
    }),

    Components({

    }),
    basicSsl({
      /** name of certification */
      name: 'test',
      /** custom trust domains */
      domains: ['*.custom.com'],
      /** custom certification directory */
      certDir: '/Users/.../.devServer/cert'
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      'lang': fileURLToPath(new URL('./src/lang/', import.meta.url))
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

