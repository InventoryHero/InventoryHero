// src/router.d.ts
import 'vue-router';

declare module 'vue-router' {
    interface RouteMeta {
        requiresAuth?: boolean;
        requiresHousehold?: boolean;
        fillHeight?: boolean;
        title?: string;
    }
}
