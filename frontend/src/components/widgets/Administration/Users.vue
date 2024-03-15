<script lang="ts">
import {defineComponent} from "vue";
import useAxios from "@/composables/useAxios.ts";
import {AdministrationEndpoint} from "@/api/http/AdministrationEndpoint.ts";
import {User} from "@/types/api.ts";

export default defineComponent({
  name: "Users",
  setup(){
    const adminEndpoint = useAxios("administration")
    return {
      adminEndpoint: adminEndpoint.axios as AdministrationEndpoint
    }
  },
  data() {
    return {
      loading: false,
      users: [] as Array<User>
    }
  },
  mounted(){
    this.loading = true
    this.adminEndpoint.loadUsers().then((users) => {
      this.users = users
      console.log(this.users)
      this.loading = false
    })
  }
})
</script>

<template>
  <v-container :fluid="true" class="pl-0 pr-0">
    <v-data-table
        :items="users"
    />
  </v-container>
</template>

<style scoped lang="scss">

</style>