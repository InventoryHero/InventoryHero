import { createApp } from 'vue'
import App from './App.vue'
import Route1 from './views/Route1.vue'
import Default from './views/Default.vue'
import * as VueRouter from 'vue-router'
import './registerServiceWorker'

const routes = [
    {path: "/route1", component: Route1}, 
    {path: "/", component: Default}
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes,
});




createApp(App).use(router).mount('#app')
