const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  pwa: {
    name: 'InventoryHero',
    themeColor: '#d1bdff',
    msTileColor: '#d1bdff',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: '#d1bdff',
    workboxOptions: {
      skipWaiting: true
    }
  },

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
})
