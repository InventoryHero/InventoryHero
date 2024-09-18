/// <reference types="vite/client" />
import type { Notifications } from '@kyvg/vue3-notification';
import {FunctionalComponent} from "vue";
import 'pinia'
import 'vue-router';
import { Router } from 'vue-router'
import { Vuetify } from 'vuetify'
import { I18n } from "vue-i18n";


export {}

declare module 'vue-qr/src/packages/vue-qr.vue';

declare module 'vue'{
    export interface GlobalComponents {
        Notifications: FunctionalComponent<Notifications>;
    }
}

declare module 'pinia' {
    export interface PiniaCustomProperties {
        // type the router added by the plugin above (#adding-new-external-properties)
        $router: Router,
        vuetify: Vuetify,
        i18n: I18n
    }
}



declare module 'vue-router' {
    interface RouteMeta {
        fillHeight?: boolean
        requiresAuth?: boolean
        requiresHousehold?: boolean,
        requiresAdmin?: boolean,
        tokenized?: boolean,
        key?: string
    }
}

