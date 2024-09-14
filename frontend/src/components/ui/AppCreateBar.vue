<script lang="ts">
import {defineComponent} from 'vue'
import {useRoute} from "vue-router";

export default defineComponent({
  name: "AppCreateBar",
  setup(){
    const route = useRoute();
    return {route}
  },
  computed: {
    createProduct(){
      return this.route.path === "/create/product"
    },
    createBox(){
      return this.route.path === "/create/box"
    },
    createLocation(){
      return this.route.path === "/create/location"
    }
  },
  data(){
    return {
      back: ""
    }
  },
  methods:{
    switchView(view: string){
      this.$router.push(`/create/${view}`)
    }
  },
  mounted(){
    this.back = this.$router.options.history.state.back

    if(this.back.includes("/create")){
      this.back = "/"
    }
  }
})
</script>

<template>
  <<v-app-bar
      density="compact"
      v-if="true"
  >
    <template #prepend>
      <v-icon
          icon="mdi-close"
          class="ms-2"
          @click="$router.push(back)"
      />
    </template>


    <template #title>
      <v-slide-group
          :show-arrows="false"
          class="fill-height"
      >
        <v-slide-group-item
        >
          <v-btn
              :class="{
                'tab-active': createProduct
              }"
              class="fill-height"
              variant="plain"
              color="primary"
              @click="switchView('product')"
              prepend-icon="mdi-cart"
          >
            {{ $t('add.product.tab') }}
          </v-btn>

        </v-slide-group-item>

        <v-slide-group-item
        >
          <v-btn
              :class="{
                'tab-active': createBox
              }"
              style="height: 100% !important;"
              class="fill-height"
              variant="plain"
              color="primary"
              @click="switchView('box')"
              prepend-icon="mdi-package-variant"
          >
            {{ $t('add.box.tab') }}
          </v-btn>
        </v-slide-group-item>

        <v-slide-group-item
        >
          <v-btn
              :class="{
                'tab-active': createLocation
              }"
              class="fill-height"
              variant="plain"
              color="primary"
              @click="switchView('location')"
              prepend-icon="mdi-archive-marker"
          >
            {{ $t('add.location.tab') }}
          </v-btn>
        </v-slide-group-item>
      </v-slide-group>
    </template>
  </v-app-bar>
</template>

<style scoped lang="scss">
:deep(.v-toolbar-title){
  height: 100% !important;
}
:deep(.v-toolbar-title__placeholder){
  height: 100% !important;
}
.tab-active{
  border-bottom: 1px solid rgba(var(--v-theme-primary), 1);
  border-radius: 0 !important;
}
</style>