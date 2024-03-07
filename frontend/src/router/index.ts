
import {createRouter, createWebHistory} from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import Login from "@/views/Login.vue"
import {useAuthStore} from "@/store";
import Products from "@/views/Products.vue";
import Settings from "@/views/Settings.vue";
import Account from "@/views/Account.vue";
import Household from "@/views/Household.vue";
import Create from "@/views/Create.vue";
import Boxes from "@/views/Boxes.vue";
import Locations from "@/views/Locations.vue";
import NotFound from "@/views/NotFound.vue";
import Logout from "@/views/Logout.vue";
import CreateProductCard from "@/components/widgets/Create/CreateProductCard.vue";
import CreateBoxCard from "@/components/widgets/Create/CreateBoxCard.vue";
import CreateLocationCard from "@/components/widgets/Create/CreateLocationCard.vue";
import {i18n} from "@/lang";
import Confirmation from "@/views/Confirmation.vue";
import Join from "@/views/Join.vue";
import {notify} from "@kyvg/vue3-notification";

export const router = createRouter({
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
        fillHeight: true
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
      component: Logout
    },
    {
      path: '/:pathMatch(.*)*',
      name: '404',
      component: NotFound
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

router.beforeEach(async (to, from) => {

  // TODO FIX FETCH HOUSEHOLD ERROR WHEN LOGGING OUT
  if(to.path === "/logout")
    return;


  const authStore = useAuthStore();

  const loggedIn = authStore.isAuthorized()

  if(!loggedIn){
    if(to.path === "/login") {
      return
    }
    if(to.path.startsWith("/confirmation")){
      return
    }
    authStore.setReturnUrl(to.fullPath)
    return "/login"
  }

  if(to.path === "/login")
    return "/"
  if(to.path.startsWith("/confirmation"))
    return "/"

  if(to.meta.requiresHousehold && (authStore.household === -1)){
    authStore.setReturnUrl(to.fullPath)
    return "/households"
  }
})

router.beforeEach(async (to, from) => {
  document.title = to.meta?.title ?? i18n.global.t('app.title')
  notify({
    group: 'newContent', // clean only the foo group
    clean: true,
  });
})

declare module 'vue-router' {
  interface RouteMeta {
    fillHeight?: boolean
    requiresAuth?: boolean
    requiresHousehold?: boolean
  }
}
