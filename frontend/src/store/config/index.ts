import { defineStore } from 'pinia'
import {useLocalStorage} from "@vueuse/core";
import vuetify from "@/plugins/vuetify.ts";
import {TinyColor} from "@ctrl/tinycolor";
import {i18n} from "@/lang";
import {Locale} from 'vue-i18n'


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
                language: "default",
                transitions: true
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
            this.config.transitions = true;
        },
        languageChange(newLanguage: string){
            if(newLanguage === "default"){
                this.config.language = "default"
                i18n.global.locale = (navigator.language || navigator.userLanguage)
                return
            }
            if(i18n.global.availableLocales.includes(newLanguage)){
                this.config.language = newLanguage
                i18n.global.locale = this.config.language
            }
        },
        init(){
            this.themeChange(this.config.theme)
            this.languageChange(this.config.language)
        },
        toggleTransitions(){
            this.config.transitions = !this.transitions
        }
    },
    getters: {
        theme: state => state.config.theme.dark,
        color: state => state.config.theme.color,
        dock: state => state.config.useDock,
        language: state => state.config.language,
        transitions: state => state.config.transitions
    }
})