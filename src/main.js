import { createApp } from 'vue'
import App from './App.vue'
import * as VueRouter from 'vue-router'
import './registerServiceWorker'

import 'vue-material-design-icons/styles.css'
import "@/global.css"
import vuetify from "./plugins/vuetify";
import withUUID from "vue-uuid";

import LoginView from '@/views/LoginView';
import HomeView from '@/views/HomeView';
import RegisterView from '@/views/RegisterView';
import NotFoundComponent from "@/components/NotFoundComponent.vue";
import LocationsOverview from '@/views/LocationsOverviewView';
import ProductsOverview from '@/views/ProductsOverviewView';
import BoxesOverview from '@/views/BoxesOverviewView';



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
        props: route => ({room_id: route.query.room_id, box_id: route.query.box_id}),
        alias: "/productsFilteredView"
    },
    {
        path: "/BoxesOverview",
        name: "boxes",
        component: BoxesOverview,
        props: route => ({room_id: route.query.room_id}),
        alias: '/boxesFilteredView'
    }
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes
});

createApp(App).use(router).use(vuetify).use(withUUID).mount('#app')

