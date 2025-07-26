
import {createRouter, createWebHistory} from "vue-router";
import {routes} from 'vue-router/auto-routes'
import useAuthStore from "@/store/useAuthStore";
import useConfigStore from "@/store/useConfigStore.ts"
import useContentRefreshStore from "@/store/useContentRefreshStore.ts";
import {i18n} from "@/lang";
//@ts-expect-error cannot be found, but it is there
import { setupLayouts } from 'virtual:generated-layouts'

const vueRouter = createRouter({
  history: createWebHistory(),
  routes: setupLayouts(routes)
})

vueRouter.beforeEach(async (to, from) => {
  const allowAuthorized = to.meta.allowAuthorized ?? true
  const requiresAuth = to.meta.requiresAuth ?? true
  const requiresHousehold = to.meta.requiresHousehold ?? true

  const authStore = useAuthStore();
  const loggedIn = await authStore.isAuthorized()
  const household = authStore.household
  const configStore = useConfigStore();
  console.log(to)


  if(loggedIn && !allowAuthorized){
    return "/"
  }

  if(!loggedIn && requiresAuth){

    return {
      path: "/login",
      query: {
        redirect: to.fullPath === "/logout" ? '/' : to.fullPath,
      }
    }
  }

  if(!household && requiresHousehold){
    return {path: "/households", query: {redirect: to.fullPath}}
  }

  if(to.name === "/login/register" && !configStore.registrationAllowed){
    return {path: "/login"}
  }


  // TODO ADMIN
  /*
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
  }*/
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



export default vueRouter


