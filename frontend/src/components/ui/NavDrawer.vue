<script lang="ts">
import {defineComponent} from 'vue'
import {isMobile} from "mobile-device-detect";
import NavItem from "@/components/ui/NavItem.vue";
import NavList from "@/components/common/NavList.vue";
import {useRoute} from "vue-router";
import AppNavListAdmin from "@/components/ui/AppNavListAdmin.vue";

export default defineComponent({
  name: "NavDrawer",
  components: {AppNavListAdmin, NavList, NavItem},
  setup(){
    const route = useRoute()
    return {route}
  },
  watch:{

  },
  props:{
    visible: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    model: {
      get(): boolean {
        return this.visible
      },
      set(value: boolean){
        this.$emit('update:modelValue', value)
      }
    },
    admin(){
      return this.route.path.includes("/administration")
    },
    isMobile(){
      return isMobile
    }
  }
})
</script>

<template>
<v-navigation-drawer
  v-model="model"
  :temporary="true"
>
  <v-list
  >
    <nav-list
        v-if="!admin"
        :is-dock="false"
    />
    <app-nav-list-admin
        v-else
    />
  </v-list>
</v-navigation-drawer>
</template>

<style scoped lang="scss">

</style>