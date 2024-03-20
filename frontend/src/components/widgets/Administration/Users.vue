<script lang="ts">
import {defineComponent} from "vue";
import useAxios from "@/composables/useAxios.ts";
import {AdministrationEndpoint} from "@/api/http/AdministrationEndpoint.ts";
import {User} from "@/types/api.ts";
import {useDisplay} from "vuetify";

export default defineComponent({
  name: "Users",
  setup(){
    const adminEndpoint = useAxios("administration")
    const {mobile} = useDisplay()
    return {
      mobile,
      adminEndpoint: adminEndpoint.axios as AdministrationEndpoint
    }
  },
  computed:{
    headers() {
      if(this.mobile){
        return [
          {
            title: "Username",
            value: "username"
          },
          {
            title: "E-Mail",
            value: "email"
          }
        ]
      }
      return
    }
  },
  data() {
    return {
      loading: false,
      users: [] as Array<User>
    }
  },
  methods:{
    clickRow(item: User){
      console.log(item)
    }
  },
  mounted(){
    this.loading = true
    console.log(this.mobile)
    this.adminEndpoint.loadUsers().then((users) => {
      this.users = users
      this.loading = false
    })
  }
})
</script>

<template>
  <v-container :fluid="true" class="pl-0 pr-0">
    <v-data-table
        :headers="headers"
        :items="users"
        @click:row="(_: any, item: any) => clickRow(item.item)"
    />
  </v-container>
</template>

<style scoped lang="scss">

</style>