import { createApp } from 'vue'
import App from './App.vue'
import * as VueRouter from 'vue-router'
import './registerServiceWorker'

import "@/global.css"

import LoginView from '@/views/LoginView';
import HomeView from '@/views/HomeView';

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
    }
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes,
});

createApp(App).use(router).mount('#app')