import {argbFromHex, hexFromArgb, themeFromSourceColor} from "@material/material-color-utilities";

export default  (sourceColorHex: string) => {
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
