import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'
import useAuthStore from '@/stores/useAuthStore'
import useConfigStore from '@/stores/useConfigStore'
import useContentRefreshStore from '@/stores/useContentRefreshStore'
import { i18n } from '@/plugins/i18n'
//@ts-expect-error cannot be found, but it is there
import { setupLayouts } from 'virtual:generated-layouts'

const router = createRouter({
  history: createWebHistory(),
  routes: setupLayouts(routes)
})

router.beforeEach(async (to, from) => {
  const allowAuthorized = to.meta.allowAuthorized ?? true
  const requiresAuth = to.meta.requiresAuth ?? true
  const requiresHousehold = to.meta.requiresHousehold ?? true
  const requiresAdmin = to.meta.layout === 'admin'

  const authStore = useAuthStore()
  const configStore = useConfigStore()

  const { household, authorized, user } = storeToRefs(authStore)
  const { registrationAllowed } = storeToRefs(configStore)

  await authStore.whoami()
  await authStore.getDefaultHousehold()

  if (authorized.value && !allowAuthorized) {
    return '/'
  }

  if (!authorized.value && requiresAuth) {
    return {
      path: '/login',
      query: {
        redirect: to.fullPath === '/logout' ? '/' : to.fullPath
      }
    }
  }

  if (!household.value && requiresHousehold) {
    return { path: '/households', query: { redirect: to.fullPath } }
  }

  if (to.name === '/login/register' && !registrationAllowed.value) {
    return { path: '/login' }
  }

  if (requiresAdmin && !(user.value?.admin ?? false)) {
    // TODO NOTIFICATION
    return {
      path: '/'
    }
  }
})

router.beforeEach(async (to, from) => {
  const contentRefreshStore = useContentRefreshStore()
  contentRefreshStore.clearBanner()

  document.title = (to.meta?.title ?? i18n.global.t('app.title')) as string
  /*notify({
    group: 'newContent',
    clean: true,
  });*/
})

router.beforeEach((to, from) => {
  /*
  For every layer in the pages there needs to be an index.vue, see: 
  https://github.com/JohnCampionJr/vite-plugin-vue-layouts/issues/148

  hopefully this is soon fixed in https://github.com/loicduong/vite-plugin-vue-layouts-next/issues/6

  this navigation guard prevents routing to these routes, it just redirects to the homepage
  those routes should only be accessible by directly entering a url (i.e. they should not be reachable by "correct" navigation inside the app)
  */
  if (to.meta.emptyRoute ?? false) {
    return '/'
  }
})

export default router
