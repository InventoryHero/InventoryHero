<script lang="ts">
import {defineComponent} from "vue";
import {useAuthStore} from "@/store";
import {i18n} from "@/lang";
import {notify} from "@kyvg/vue3-notification";

export default defineComponent({

  setup(){
    const authStore = useAuthStore()
    return {
      authStore
    }
  },
  beforeRouteEnter(to, from){
    const authStore = useAuthStore()
    if(!authStore.isAdmin){
      notify({
        title: i18n.global.t('toasts.titles.error.no_access'),
        text: i18n.global.t('toasts.text.error.no_access'),
        type: "error"
      })
      return "/"
    }
  },
  props: {

  }
})
</script>

<template>
  <router-view />
</template>

<style scoped lang="scss">

</style>