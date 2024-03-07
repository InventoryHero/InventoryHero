<script lang="ts">
import {defineComponent} from 'vue'
import {useAuthStore} from "@/store";

export default defineComponent({
  name: "Logout",
  data(){
    return{
      loggingOut: true
    }
  },
  beforeRouteEnter(){
    const authStore = useAuthStore();
    if(authStore.isAuthorized())
      return "/"

    if(!authStore.isAuthorized() && !authStore.userSet)
      return "/login"
  }
})
</script>

<template>
  <v-row>
    <v-dialog
        :fullscreen="true"
        :persistent="true"
        v-model="loggingOut"
    >
      <v-row
          justify="center"
          class="fill-height align-content-center"
      >
        <v-col
            cols="11"
            lg="6"
        >
          <v-card
              class="d-flex flex-column justify-center align-center pb-4 pt-4"
          >
            {{ $t('logging_out') }}
            <v-progress-circular
                width="8"
                size="90"
                indeterminate
                color="primary"
                class="mt-2"
            />
          </v-card>
        </v-col>
      </v-row>
    </v-dialog>
  </v-row>
</template>

<style scoped lang="scss">

</style>