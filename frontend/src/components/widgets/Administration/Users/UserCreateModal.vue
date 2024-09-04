<script lang="ts">
import {defineComponent, PropType} from "vue";
import {useDisplay} from "vuetify";
import {User} from "@/types/api.ts";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {useGeneralSocketStore} from "@/store";

export default defineComponent({
  name: "UserCreateModal",
  setup(){
    const {mobile} = useDisplay()
    const {axios} = useAxios("user")

    return {
      mobile,
      userEndpoint: axios as UserEndpoint
    }
  },
  emits:{
    'created:user'(_: User){
      return true
    },
    'update:modelValue'(value: boolean){
      return true
    }
  },
  computed:{
    active: {
      get(){
        return this.modelValue
      },
      set(value: boolean){
        this.$emit('update:modelValue', value)
      }
    },
    user(){
      return this.modelValue
    },
    fullscreen(){
      return this.mobile
    }
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  data(){
    return {
      loading: false
    }
  },
  methods:{
    async createNewUser(newUser: Partial<User>){
      if(this.user === undefined){
        return
      }
      this.loading = true;
      const {success, user} = await this.userEndpoint.createUser(newUser)
      this.loading = false
      if(!success){
        return;
      }
      this.$notify({
        title: this.$t(`toasts.titles.success.user_created`, {username: user.username}),
        text: this.$t(`toasts.text.success.user_created`),
        type: "success"
      })
      this.active = false
      this.$emit('created:user', user)
    }
  }
})
</script>

<template>
  <v-dialog
      v-model="active"
      :fullscreen="fullscreen"
      :scrim="!mobile"
      :persistent="true"
      :no-click-animation="true"
  >
    <v-expand-transition>
      <v-row
          :no-gutters="true"
          justify="center"
          class="fill-height"
          v-if="active"
      >
        <v-col
            lg="6"
            cols="12"
        >
          <user-card
              height="100%"
              :loading="loading"
              :edit="false"
              :title="$t('administration.users.create_title')"
              @close="active=false"
              @click:save="createNewUser"
          >
          </user-card>
        </v-col>
      </v-row>
    </v-expand-transition>
  </v-dialog>
</template>


<style scoped lang="scss">
</style>