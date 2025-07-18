import { defineStore } from 'pinia'
import {useLocalStorage} from "@vueuse/core";
import {TinyColor} from "@ctrl/tinycolor";
import {Theme} from "./types"

import {
    argbFromHex,
    hexFromArgb,
    themeFromSourceColor,
    TonalPalette,
} from "@material/material-color-utilities";
import {useTheme} from "vuetify/framework";
import useGenerateMaterialYouTheme from "@/composables-new/useGenerateMaterialYouTheme.ts";




export const useConfigStore = defineStore('config', {
    state: () => {
        return {
            initialized: false,
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
            const newThemes = useGenerateMaterialYouTheme(this.config.theme.color)
            this.vuetify.theme.themes.value.light.colors = newThemes.light.colors
            this.vuetify.theme.themes.value.dark.colors = newThemes.dark.colors
            this.vuetify.theme.global.name.value = this.config.theme.dark ? 'dark' : 'light'
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
            this.initialized = true
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