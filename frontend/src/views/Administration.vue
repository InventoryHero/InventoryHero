<script setup lang="ts">
/*import {useAuthStore} from "@/store";
import {notify} from "@kyvg/vue3-notification";


const authStore = useAuthStore()
const router = useRouter()
const {t} = useI18n()

if(!authStore.isAdmin){

  router.push("/").then(() => {
    notify({
      title: t('toasts.titles.info.insufficient_permissions'),
      text: t('toasts.text.info.insufficient_permissions'),
      type: 'info'
    })
  })
}*/

</script>

<template>
  <router-view />
</template>

<style scoped lang="scss">

</style>