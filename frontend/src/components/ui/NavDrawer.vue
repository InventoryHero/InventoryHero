<script lang="ts">
import {defineComponent} from 'vue'
import {useRoute} from "vue-router";

export default defineComponent({
  name: "NavDrawer",
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
  }
})
</script>

<template>
<v-navigation-drawer
  v-model="model"
  :temporary="true"
>
  <v-list
      density="compact"
      nav
  >
    <v-list-item
        to="/"
        prepend-icon="mdi-home"
        :title="$t('nav.home')"
        color="primary"
    />
    <template v-if="!admin">
      <v-list-item
          to="/products"
          prepend-icon="mdi-cart"
          :title="$t('nav.products')"
          color="primary"
      />
      <v-list-item
          to="/storage/boxes"
          prepend-icon="mdi-package-variant"
          :title="$t('nav.boxes')"
          color="primary"
      />
      <v-list-item
          to="/storage/locations"
          prepend-icon="mdi-archive-marker"
          :title="$t('nav.location')"
          color="primary"
      />
      <v-list-item
          to="/create"
          prepend-icon="mdi-plus-box"
          :title="$t('nav.create')"
          color="primary"
      />
    </template>
    <template v-else>
      <v-list-item
          to="/administration"
          prepend-icon="mdi-view-dashboard"
          :title="$t('nav.admin.overview')"
          color="primary"
          :exact="true"
      />
      <v-list-item
          to="/administration/users"
          prepend-icon="mdi-account-group"
          :title="$t('nav.admin.overview')"
          color="primary"
          :exact="true"
      />
    </template>
  </v-list>


</v-navigation-drawer>
</template>

<style scoped lang="scss">

</style>