import { defineStore } from 'pinia'
import {useLocalStorage} from "@vueuse/core";
import vuetify from "@/plugins/vuetify.ts";
import {TinyColor} from "@ctrl/tinycolor";




export const useConfigStore = defineStore('config', {
    state: () => {
        return {
            config: useLocalStorage("config", {
                version: 1.0,
                theme: {
                    name: "InventoryHero",
                    dark: true,
                    color: "#2196f3"
                } as Theme,
                useDock: true,
                language: "en"
            })
        }
    },
    actions: {
        themeChange(newTheme: Partial<Theme>){
            this.config.theme = {
                ...this.config.theme,
                ...newTheme
            }
            const theme = this.config.theme.dark ? "dark" : "light"
            const primary = new TinyColor(this.config.theme.color);


            vuetify.theme.themes.value[theme].colors.primary = this.config.theme.color
            vuetify.theme.themes.value[theme].colors.secondary = primary.desaturate(5).darken(10).toHexString()
            vuetify.theme.global.name.value = theme

            document?.querySelector('meta[name="theme-color"]')?.setAttribute("content", this.config.theme.color);

        },
        toggleDock(useDock: boolean){
            this.config.useDock = useDock
        },
        reset(){
            // TODO LOAD CONFIG FROM config.json
            this.themeChange({
                name: "InventoryHero",
                dark: true,
                color: "#2196f3"
            })
            this.config.useDock = true;
        },

        init(){
            this.themeChange(this.config.theme)

        }
    },
    getters: {
        theme: state => state.config.theme.dark,
        color: state => state.config.theme.color,
        dock: state => state.config.useDock
    }
})