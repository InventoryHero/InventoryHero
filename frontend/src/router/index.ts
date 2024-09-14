
import {createRouter, createWebHistory} from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import Login from "@/views/Login.vue"
import {useAuthStore} from "@/store";
import Settings from "@/views/Settings.vue";
import Account from "@/views/Account.vue";
import Household from "@/views/Household.vue";
import Create from "@/views/Create.vue";
import Locations from "@/views/Locations.vue";
import Logout from "@/views/Logout.vue";
import CreateProductCard from "@/components/widgets/Create/CreateProductCard.vue";
import CreateBoxCard from "@/components/widgets/Create/CreateBoxCard.vue";
import CreateLocationCard from "@/components/widgets/Create/CreateLocationCard.vue";
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
    {
      path: "/households",
      name: "households",
      component: Household,
      meta: {
        requiresAuth: true,
        fillHeight: true,
        title: i18n.global.t('titles.households')
      }
    },
    {
      path: "/create",
      component: Create,
      redirect: '/create/product',
      children:[
        {
          path: 'product',
          name: "create.product",
          component: CreateProductCard,
        },
        {
          path: 'box',
          name: "Create Box",
          component: CreateBoxCard,
        },
        {
          path: 'location',
          name: "Create Location",
          component: CreateLocationCard,
        },
      ],
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

vueRouter.beforeEach(async (to) => {
  const authStore = useAuthStore();
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

  if(to.meta.requiresHousehold && (authStore.household === -1)){
    authStore.setReturnUrl(to.fullPath)
    return "/households"
  }

  if((to.meta.requiresAdmin ?? false) && !authStore.isAdmin) {
    notify({
      title: i18n.global.t('toasts.titles.info.insufficient_permissions'),
      text: i18n.global.t('toasts.text.info.insufficient_permissions'),
      type: 'info'
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


