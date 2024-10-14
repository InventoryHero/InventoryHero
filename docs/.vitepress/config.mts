import { defineConfig } from 'vitepress'
import type { HeadConfig } from 'vitepress'

const head: HeadConfig[] = [['link', { rel: 'icon', href: '/logo.ico' }]]

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "InventoryHero",
  description: "A simple to use inventory software",
  head,
  themeConfig: {
    logo: '/logo.ico',
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      //{ text: 'Examples', link: '/markdown-examples' }
    ],

    sidebar: [
      {
        
        text: 'Documentation',
        items: [
          { text: 'About', link: '/intro/about' },
          //{ text: 'Runtime API Examples', link: '/api-examples' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/InventoryHero/InventoryHero' }
    ]
  }
})
