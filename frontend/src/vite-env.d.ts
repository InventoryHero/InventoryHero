/// <reference types="vite/client" />
import {TinyEmitter} from "tiny-emitter";
import type { Notifications } from '@kyvg/vue3-notification';
import {FunctionalComponent} from "vue";
import 'pinia'
import type { Router } from 'vue-router'

export {}

declare module 'vue'{
    interface ComponentCustomProperties {
        $emitter: TinyEmitter
    }
    export interface GlobalComponents {
        Notifications: FunctionalComponent<Notifications>;
    }
}

declare module 'pinia' {
    export interface PiniaCustomProperties {
        // type the router added by the plugin above (#adding-new-external-properties)
        $router: Router
    }
}

