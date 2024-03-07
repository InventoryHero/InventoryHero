<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "NavList",
  props:{
    isDock: {
      type: Boolean,
      required: true
    }
  }
})
</script>

<template>
  <nav-item
      route="/"
      icon="fa:fas fa-home"
  >
    <template v-if="!isDock" #title>
      {{ $t('nav.home') }}
    </template>
  </nav-item>

  <nav-item
      route="/products"
      icon="fa:fas fa-shopping-cart"
  >
    <template v-if="!isDock" #title>
      {{$t('nav.products')}}
    </template>
  </nav-item>

  <nav-item
    v-if="isDock"
    route="/create"
    icon="fa:fas fa-plus"
    :exact="false"
  />

  <nav-item
      icon="fa:fas fa-boxes"
      route="/storage/boxes"
      :exact="false"
  >
    <template v-if="!isDock" #title>
      {{ $t('nav.boxes') }}
    </template>
  </nav-item>

  <nav-item
      icon="fa:fas fa-building"
      route="/storage/locations"
      :exact="false"
  >

    <template v-if="!isDock" #title>
      {{ $t('nav.location') }}
    </template>
  </nav-item>

  <nav-item
      v-if="!isDock"
      route="/create"
      icon="fa:fas fa-plus"
      :title="$t('nav.create_new') "
  >

  </nav-item>
</template>

<style scoped lang="scss">

</style>