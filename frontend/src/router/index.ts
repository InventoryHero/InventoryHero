
import {createRouter, createWebHistory} from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import Login from "@/views/Login.vue"
import {useAuthStore, useNotificationStore} from "@/store";
import Settings from "@/views/Settings.vue";
import Account from "@/views/Account.vue";
import Create from "@/views/Create.vue";
import Locations from "@/views/Locations.vue";
import Logout from "@/views/Logout.vue";
import {i18n} from "@/lang";
import Confirmation from "@/views/Confirmation.vue";
import Join from "@/views/Join.vue";
import {notify} from "@kyvg/vue3-notification";
import Users from "@/components/widgets/Administration/Users.vue";
import Overview from "@/components/widgets/Administration/Overview.vue";

import passwordReset from "./routes/passwordReset.ts";
import Products from "@/views/Products.vue";
import Boxes from "@/views/Boxes.vue";
import RouteNotFound from "@/views/RouteNotFound.vue";
import {householdsOverview, editHousehold} from "@/router/routes/household.ts";



const vueRouter =  createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: Login,
      meta: {
        requiresAuth: false,
        fillHeight: false
      }
    },
    {
      path: "/confirmation/:code",
      name: "confirmation",
      component: Confirmation,
      props: true,
      meta: {
        requiresAuth: false,
        fillHeight: true,
        requiresHousehold: false,
        tokenized: true
      }
    },
    {
      path: "/join/:code",
      name: "join",
      component: Join,
      props: true,
      meta: {
        requiresAuth: true,
        fillHeight: false,
        requiresHousehold: false
      }
    },
    {
      path: "/",
      name: "home",
      component: Dashboard,
      meta: {
        requiresAuth: true,
        requiresHousehold: true,
        fillHeight: false
      }
    },
    {
      path: "/products",
      children:[
        {
          path: '',
          name: "products",
          component: Products,
        },
        {
          path: ':preselectedProduct/:filteredFrom',
          component: Products,
          props: true
        }
      ],
      meta: {
        requiresAuth: true,
        requiresHousehold: true,
        fillHeight: true,
        title: i18n.global.t('titles.products')
      },
    },
    {
      path: "/storage/boxes",
      children:[
        {
          path: '',
          name: "Boxes",
          component: Boxes,
        },
        {
          path: ':preselectedBox',
          component: Boxes,
          props: true
        },
        {
          path: ':preselectedBox/:filteredFrom',
          component: Boxes,
          props: true
        }
      ],
      meta: {
        requiresAuth: true,
        requiresHousehold: true,
        fillHeight: true,
        title: i18n.global.t('titles.boxes')
      },
    },
    {
      path: "/storage/locations",
      children:[
        {
          path: '',
          name: "Locations",
          component: Locations,
        },
        {
          path: ':preselectedLocation/:filteredFrom',
          component: Locations,
          props: true
        },
        {
          path: ':preselectedLocation',
          component: Locations,
          props: true
        }
      ],
      meta: {
        requiresAuth: true,
        requiresHousehold: true,
        fillHeight: true,
        title: i18n.global.t('titles.locations')
      }
    },
    {
      path: "/settings",
      name: "settings",
      component: Settings,
      meta: {
        requiresAuth: false,
        requiresHousehold: false,
        fillHeight: false,
        title: i18n.global.t('titles.settings')
      }
    },
    {
      path: "/account",
      name: "account",
      component: Account,
      meta: {
        requiresAuth: true,
        fillHeight: false,
        title: i18n.global.t('titles.account')
      }
    },
    householdsOverview,
    editHousehold,
    {
      path: "/create",
      component: Create,
      meta:{
        requiresAuth: true,
        requiresHousehold: true,
        fillHeight: true,
        transition: 'slide',
        title: i18n.global.t('titles.create')
      }
    },
    {
      path: '/logout',
      name: "logout",
      component: Logout,
      meta: {
        requiresHousehold: false,
        requiresAuth: true,
        fillHeight: true
      }
    },
    {
      path: "/administration",
      children: [
        {
          path: "",
          name: "AdministrationLanding",
          component: Overview
        },
        {
          path: "users",
          name: "AdministrationUsers",
          component: Users
        }
      ],
      meta:{
        requiresAuth: true,
        requiresAdmin: true,
        fillHeight: false,
        transition: 'slide',
        title: i18n.global.t('titles.administration')
      }
    },
    passwordReset,
    {
      path: '/not-found',
      component: RouteNotFound,
      name: "route-not-found",
      meta: {
        fillHeight: true,
        requiresAuth: false,
        requiresAdmin: false,
        requiresHousehold: false,
        transition: 'slide'
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: '404',
      redirect: '/not-found'
    }

  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

vueRouter.beforeEach(async (to, from) => {
  const authStore = useAuthStore();
  const notificationStore = useNotificationStore()
  const loggedIn = await authStore.isAuthorized()
  if(!loggedIn){
    if(to.path === "/login") {
      return
    }
    if(!(to.meta.requiresAuth ?? true)){
      return
    }
    if(to.path !== "/logout"){
      authStore.setReturnUrl(to.fullPath)
    }
    return "/login"
  }

  if(to.path === "/login") {
    return "/"
  }

  if(to.meta.requiresHousehold && !authStore.household){
    authStore.setReturnUrl(to.fullPath)
    return "/households"
  }
  if(!(to.meta.requiresAdmin ?? false)){
    return
  }

  await authStore.fetchPermissions()
  if((to.meta.requiresAdmin ?? false) && !authStore.isAdmin) {
    notificationStore.addNotification({
      title: i18n.global.t('toasts.titles.warning.insufficient_permissions'),
      text: i18n.global.t('toasts.text.warning.insufficient_permissions'),
      type: 'warning'
    })
    return "/"
  }
})

vueRouter.beforeEach(async (to) => {
  document.title = (to.meta?.title ?? i18n.global.t('app.title')) as string
  notify({
    group: 'newContent',
    clean: true,
  });
})

export default vueRouter


