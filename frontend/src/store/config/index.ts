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


function generateExactM3Themes(sourceColorHex: string) {
    const m3Theme = themeFromSourceColor(argbFromHex(sourceColorHex));
    const toHex = (color: number) => hexFromArgb(color);

    // A helper to create the full color set for either light or dark mode
    const createColors = (scheme: 'light' | 'dark') => {
        const isLight = scheme === 'light';
        return {
            // Your exact background and surface tones
            background: toHex(m3Theme.palettes.neutral.tone(isLight ? 90 : 10)),
            surface: toHex(m3Theme.palettes.neutral.tone(isLight ? 99 : 6)),
            'surface-dim': toHex(m3Theme.palettes.neutral.tone(isLight ? 87 : 6)),
            'surface-bright': toHex(m3Theme.palettes.neutral.tone(isLight ? 99 : 24)),
            'surface-light': toHex(m3Theme.palettes.neutral.tone(isLight ? 92 : 24)),

            // Standard on-colors
            'on-background': toHex(m3Theme.schemes[scheme].onBackground),
            'on-surface': toHex(m3Theme.schemes[scheme].onSurface),
            'on-primary': toHex(m3Theme.schemes[scheme].onPrimary),
            'on-secondary': toHex(m3Theme.schemes[scheme].onSecondary),
            'on-tertiary': toHex(m3Theme.schemes[scheme].onTertiary),

            // Standard primary, secondary, tertiary, error
            primary: toHex(m3Theme.schemes[scheme].primary),
            secondary: toHex(m3Theme.schemes[scheme].secondary),
            tertiary: toHex(m3Theme.schemes[scheme].tertiary),

            // Standard outline colors
            outline: toHex(m3Theme.schemes[scheme].outline),
            'outline-variant': toHex(m3Theme.schemes[scheme].outlineVariant),

            info: isLight ? '#2196F3' : '#2196F3',
            'on-info': '#FFFFFF',
            success: isLight ? '#4CAF50' : '#4CAF50',
            'on-success': '#FFFFFF',
            warning: isLight ? '#FB8C00' : '#FB8C00',
            'on-warning': '#FFFFFF',
            error: isLight ? '#B00020' : '#ffb4ab',
            'on-error': isLight ? '#FFFFFF' : '#690005',
            accent: toHex(m3Theme.schemes[scheme].secondaryContainer),
        };
    };

    // --- Return the complete themes object ---
    return {
        light: {
            dark: false,
            colors: createColors('light'),
            variables: { 'overlay-background': '#181d14' },
        },
        dark: {
            dark: true,
            colors: createColors('dark'),
            variables: { 'overlay-background': '#181d14' },
        },
    };
}


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

            const newThemes = generateExactM3Themes(this.config.theme.color);
            this.vuetify.theme.themes.value.light.colors = newThemes.light.colors;
            this.vuetify.theme.themes.value.dark.colors = newThemes.dark.colors;
            this.vuetify.theme.global.name.value = this.config.theme.dark ? 'dark' : 'light';
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