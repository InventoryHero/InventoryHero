import { createApp } from 'vue'
import App from './App.vue'
import * as VueRouter from 'vue-router'
import './registerServiceWorker'

import 'vue-material-design-icons/styles.css'
import "@/global.css"

import LoginView from '@/views/LoginView';
import HomeView from '@/views/HomeView';
// import ProductsOverviewView from '@/views/ProductsOverviewView';

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
    // {
    //     path: "/productsOverview",
    //     name: "productsOverview",
    //     component: ProductsOverviewView
    // }
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes,
});

createApp(App).use(router).mount('#app')