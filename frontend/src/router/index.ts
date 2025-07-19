
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


