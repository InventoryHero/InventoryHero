import { createApp } from 'vue'
import App from './App.vue'
import * as VueRouter from 'vue-router'
import './registerServiceWorker'

import 'vue-material-design-icons/styles.css'
import "/node_modules/flag-icons/css/flag-icons.min.css";
import "@/global.css"
import "vue-toastification/dist/index.css";

import vuetify from "./plugins/vuetify";
import withUUID from "vue-uuid";
import LoginView from '@/views/LoginView';
import HomeView from '@/views/HomeView';
import RegisterView from '@/views/RegisterView';
import NotFoundComponent from "@/components/NotFoundComponent.vue";
import LocationsOverview from '@/views/LocationsOverviewView';
import ProductsOverview from '@/views/ProductsOverviewView';
import BoxesOverview from '@/views/BoxesOverviewView';
import Settings from '@/views/Settings';
import Toast from "vue-toastification";
import { createI18n } from 'vue-i18n'
import {localizations} from "@/lang";



const routes = [
    {
        path: "/",
        name: "login",
        component: LoginView
    },
    {
        path: "/home",
        name: "home",
        component: HomeView
    },
    {
        path: "/register",
        name: "register", 
        component: RegisterView
    },
    {
        path: '/:catchAll(.*)',
        component: NotFoundComponent,
        name: 'NotFound'
    },
    {
        path: "/LocationsOverview",
        name: "locations",
        component: LocationsOverview
    },
    {
        path:"/ProductsOverview",
        name:"products",
        component: ProductsOverview,
        //props: route => ({room_id: route.query.room_id, box_id: route.query.box_id, get_starred: route.query.starred}),
        alias: "/productsFilteredView"
    },
    {
        path: "/BoxesOverview",
        name: "boxes",
        component: BoxesOverview,
        //props: route => ({room_id: route.query.room_id}),
        alias: '/boxesFilteredView'
    },
    {
        path: "/Settings",
        name: "settings",
        component: Settings
    }
]


const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes
});

const toastOptions = {
    position: 'top-right',
    maxToasts: 2,
    pauseOnFocusLoss: false
};

function fun()
{
    return createI18n({
        locale: 'en',
        fallbackLocal: 'en',
        messages: localizations,
        useScope: 'global',
    })
}
const i18n = fun();




createApp(App).use(i18n).use(router).use(Toast, toastOptions).use(vuetify).use(withUUID).mount('#app')

