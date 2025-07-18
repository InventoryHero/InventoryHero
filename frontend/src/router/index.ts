
import {createRouter, createWebHistory} from "vue-router";
import {routes} from 'vue-router/auto-routes'
import {useAuthStore, useNotificationStore} from "@/store";
import useContentRefreshStore from "@/store/useContentRefreshStore.ts";
import {i18n} from "@/lang";
import {useModal} from "@/composables-new/useModal.ts";
const vueRouter = createRouter({
  history: createWebHistory(),
  routes: routes
})

/*const vueRouter =  createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: Login,
      meta: {
        requiresAuth: false,
        onlyUnauthorized: true,
        fillHeight: false,
        layout: Unauthorized
      }
    },
    {
      path: "/register",
      name: "register",
      component: Register,
      meta: {
        requiresAuth: false,
        onlyUnauthorized: true,
        fillHeight: false,
        layout: Unauthorized
      }
    },
    {
      path: "/forgot-password",
      name: "forgot password",
      component: ForgotPassword,
      meta: {
        requiresAuth: false,
        onlyUnauthorized: true,
        fillHeight: false,
        layout: Unauthorized
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
        tokenized: true, // TODO DEPRECATED
        layout: Tokenized
      }
    },
    {
      path: "/confirmation-missing",
      name: "missing confirmation",
      component: MissingConfirmation,
      meta: {
        requiresAuth: false,
        fillHeight: true,
        onlyUnauthorized: true,
        requiresHousehold: false
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
    ...items,
    ...boxes,
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
    households,
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
        title: i18n.global.t('titles.administration')
      }
    },
    passwordReset,
    {
      path: "/scan-qr",
      name: "QrCodeScanner",
      component: QrScanner,
      meta: {
        fillHeight: true,
        title: i18n.global.t('titles.qr_code_scanner')
      }
    },
    {
      path: '/not-found',
      component: RouteNotFound,
      name: "route-not-found",
      meta: {
        fillHeight: true,
        requiresAuth: false,
        requiresAdmin: false,
        requiresHousehold: false,
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
})*/


vueRouter.beforeEach(async (to, from) => {
  if(!to.meta.requiresAuth){
    return
  }

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

  if(to.meta.onlyUnauthorized ?? false) {
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

vueRouter.beforeEach(async (to, from) => {

  const contentRefreshStore = useContentRefreshStore()
  contentRefreshStore.clearBanner()

  document.title = (to.meta?.title ?? i18n.global.t('app.title')) as string
  /*notify({
    group: 'newContent',
    clean: true,
  });*/
})

vueRouter.beforeResolve(async to => {
  const {activeModal, closeModal, isAwaitingConfirmation, forceNavigation} = useModal()
  if(forceNavigation.value){
    closeModal()
    return
  }

  if(isAwaitingConfirmation.value){
    return false
  }
  if(activeModal.value){
    closeModal(to)
    return false
  }
})

export default vueRouter


