import { defineStore } from 'pinia'
import {useLocalStorage} from "@vueuse/core";
import {TinyColor} from "@ctrl/tinycolor";
import {Theme} from "./types"


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
                useTransitions: true,
                language: "default"
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
            this.vuetify.theme.themes.value[theme].colors.primary = this.config.theme.color
            this.vuetify.theme.themes.value[theme].colors.secondary = primary.desaturate(5).darken(10).toHexString()
            this.vuetify.theme.themes.value[theme].colors.accent = primary.desaturate(0).lighten(20).toHexString()
            this.vuetify.theme.global.name.value = theme
            document?.querySelector('meta[name="theme-color"]')?.setAttribute("content", this.config.theme.color);
        },
        toggleDock(useDock: boolean){
            this.config.useDock = useDock
        },
        toggleTransitions(useTransitions: boolean){
          this.config.useTransitions = useTransitions
        },
        reset(){
            // TODO LOAD CONFIG FROM config.json
            this.themeChange({
                name: "InventoryHero",
                dark: true,
                color: "#2196f3"
            })
            this.config.useDock = true;
            this.config.useTransitions = true;
        },
        languageChange(newLanguage: string){
            if(newLanguage === "default"){
                this.config.language = "default"
                //@ts-expect-error - I really couldn't figure out how to type newLanguage to not trigger an error
                this.i18n.global.locale = (navigator.language || navigator.userLanguage)
                return
            }
            if(this.i18n.global.availableLocales.includes(newLanguage)){
                this.config.language = newLanguage
                this.i18n.global.locale = this.config.language
            }
        },
        init(){
            this.themeChange(this.config.theme)
            this.languageChange(this.config.language)
        },
    },
    getters: {
        theme: state => state.config.theme.dark,
        color: state => state.config.theme.color,
        dock: state => state.config.useDock,
        language: state => state.config.language,
        primary: state => state.config.theme.color,
        transitions: state => state.config.useTransitions
    }
})