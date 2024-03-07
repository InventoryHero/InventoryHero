<script lang="ts">
import {defineComponent} from 'vue'
import {isMobile} from "mobile-device-detect";
import NavItem from "@/components/ui/NavItem.vue";
import NavList from "@/components/common/NavList.vue";

export default defineComponent({
  name: "NavDrawer",
  components: {NavList, NavItem},
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
    isMobile(){
      return isMobile
    }
  }
})
</script>

<template>
<v-navigation-drawer
  v-model="model"
  :rail="isMobile"
  :temprary="true"


>
  <v-list
  >
    <nav-list :is-dock="false" />
  </v-list>
</v-navigation-drawer>
</template>

<style scoped lang="scss">

</style>