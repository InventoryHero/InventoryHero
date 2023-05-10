import { createApp } from 'vue'
import App from './App.vue'
import * as VueRouter from 'vue-router'
import './registerServiceWorker'

import 'vue-material-design-icons/styles.css'
import "@/global.css"
import vuetify from "./plugins/vuetify";

import LoginView from '@/views/LoginView';
import HomeView from '@/views/HomeView';
import RegisterView from '@/views/RegisterView';
import NotFoundComponent from "@/components/NotFoundComponent.vue";
import LocationsOverview from '@/views/LocationsOverviewView';



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
    }
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes,
});

createApp(App).use(router).use(vuetify).mount('#app')

