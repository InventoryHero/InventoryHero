import {
  argbFromHex,
  hexFromArgb,
  themeFromSourceColor
} from '@material/material-color-utilities'

export default (sourceColorHex: string) => {
  const m3Theme = themeFromSourceColor(argbFromHex(sourceColorHex))
  const toHex = (color: number) => hexFromArgb(color)

  // A helper to create the full color set for either light or dark mode
  const createColors = (mode: 'light' | 'dark') => {
    const isLight = mode === 'light'

    const theme = m3Theme.schemes[mode]

    return {
      // Base surfaces
      background: toHex(theme.background),
      surface: toHex(theme.surface),
      'surface-dim': toHex(m3Theme.palettes.neutral.tone(isLight ? 87 : 6)),
      'surface-bright': toHex(m3Theme.palettes.neutral.tone(isLight ? 99 : 24)),
      'surface-light': toHex(m3Theme.palettes.neutral.tone(isLight ? 92 : 24)),

      // On colors
      'on-background': toHex(theme.onBackground),
      'on-surface': toHex(theme.onSurface),
      'on-primary': toHex(theme.onPrimary),
      'on-secondary': toHex(theme.onSecondary),
      'on-tertiary': toHex(theme.onTertiary),

      // Core color roles
      primary: toHex(theme.primary),
      secondary: toHex(theme.secondary),
      tertiary: toHex(theme.tertiary),

      // Outline
      outline: toHex(theme.outline),
      'outline-variant': toHex(theme.outlineVariant),

      // Status colors
      info: isLight ? '#2196F3' : '#2196F3',
      'on-info': '#FFFFFF',
      success: isLight ? '#4CAF50' : '#4CAF50',
      'on-success': '#FFFFFF',
      warning: isLight ? '#FB8C00' : '#FB8C00',
      'on-warning': '#FFFFFF',
      error: isLight ? '#B00020' : '#ffb4ab',
      'on-error': isLight ? '#FFFFFF' : '#690005',

      // Secondary accents
      accent: toHex(theme.secondaryContainer),

      // Inverse colors
      'inverse-surface': toHex(theme.inverseSurface),
      'inverse-on-surface': toHex(theme.inverseOnSurface),
      'inverse-primary': toHex(theme.inversePrimary),

      // Container roles (used in filled buttons, cards, etc.)
      'primary-container': toHex(theme.primaryContainer),
      'on-primary-container': toHex(theme.onPrimaryContainer),
      'secondary-container': toHex(theme.secondaryContainer),
      'on-secondary-container': toHex(theme.onSecondaryContainer),
      'tertiary-container': toHex(theme.tertiaryContainer),
      'on-tertiary-container': toHex(theme.onTertiaryContainer),

      // Surface variant
      'surface-variant': toHex(theme.surfaceVariant)
    }
  }

  // --- Return the complete themes object ---
  return {
    light: {
      dark: false,
      colors: createColors('light'),
      variables: {
        'overlay-background': toHex(m3Theme.schemes['light'].primary)
      }
    },
    dark: {
      dark: true,
      colors: createColors('dark'),
      variables: {
        'overlay-background': toHex(m3Theme.schemes['dark'].primary)
      }
    }
  }
}
