<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: "AppNavListAdmin",
})
</script>

<template>
  <nav-item
      route="/"
      icon="fa:fas fa-home"
  >
    <template #title>
      {{ $t('nav.home') }}
    </template>
  </nav-item>
  <nav-item
      route="/administration"
      icon="fa:fas fa-users"
  >
    <template #title>
      {{ $t('nav.admin.overview') }}
    </template>
  </nav-item>
  <nav-item
      route="/administration/users"
      icon="fa:fas fa-users"
  >
    <template #title>
      {{ $t('nav.admin.users') }}
    </template>
  </nav-item>
</template>

<style scoped lang="scss">

</style>