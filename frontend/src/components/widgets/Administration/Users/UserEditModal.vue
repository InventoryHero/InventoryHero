<script lang="ts">
import {defineComponent, PropType} from "vue";
import {User} from "@/types/api.ts";
import {useDisplay} from "vuetify";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";

export default defineComponent({
  name: "UserEditModal",
  setup(){
    const {mobile} = useDisplay()
    const {axios} = useAxios("user")
    return {
      mobile,
      userEndpoint: axios as UserEndpoint
    }
  },
  emits:{
    'update:modelValue'(value: User|undefined){
      return true
    }
  },
  computed:{
    active: {
      get(){
        return this.modelValue !== undefined
      },
      set(value: boolean){
        this.$emit('update:modelValue', undefined)
      }
    },
    user(){
      return this.modelValue
    },
    fullscreen(){
      console.log("mobile", this.mobile)
      return this.mobile
    }
  },
  props: {
    modelValue: {
      type: Object as PropType<Partial<User>>,
      default: undefined
    }
  },
  data(){
    return {
      loading: false
    }
  },
  methods:{
    async saveUpdatedUser(toUpdate: Partial<User>){
      this.loading = true;
      if(this.user === undefined){
        return
      }
      const {success, msg, user} = await this.userEndpoint.updateUser(toUpdate, this.user)
      this.loading = false;
      if(!success){
        return;
      }
      this.$notify({
        title: this.$t(`toasts.titles.success.${msg}`),
        text: this.$t(`toasts.text.success.${msg}`),
        type: "success"
      })
      this.$emit('update:modelValue', user)
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
            v-model="user"
            :loading="loading"
            @close="active=false"
            @click:save="saveUpdatedUser"
            :edit="true"
        >
        </user-card>
      </v-col>
    </v-row>
  </v-expand-transition>
</v-dialog>
</template>

<style scoped lang="scss">

</style>