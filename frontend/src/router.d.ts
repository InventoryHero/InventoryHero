// src/router.d.ts

import 'vue-router'

export {}

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    requiresHousehold?: boolean
    allowAuthorized?: boolean
    title?: string
    showFab?: boolean
    requiresAdmin?: boolean
  }
}
