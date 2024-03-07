<script lang="ts">
import {useAuthStore, useSocketStore} from "@/store";
import {defineComponent} from "vue";

import {getAccessToken} from "axios-jwt";

export default defineComponent({
  name: "Dashboard",
  setup(){
    const authStore = useAuthStore();
    const socketStore = useSocketStore();
    return {authStore, socketStore}
  },
  computed: {

  },
  methods: {
  }
})
</script>

<template>
  <v-row
    :no-gutters="true"
    justify="center"
  >
    <v-col
      cols="12"
      lg="8"
      class="d-flex justify-center align-center flex-column"
    >
      WELCOME TO INVENTORY HERO  😊
      <household-quick-select-card
          width="100%"
          :collapsible="true"
      />

    </v-col>
  </v-row>

</template>

<style scoped lang="scss">

</style>
