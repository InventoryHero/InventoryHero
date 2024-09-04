<script lang="ts">
import {defineComponent} from 'vue'
import {useDisplay} from "vuetify";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {User} from "@/types/api.ts";

export default defineComponent({
  name: "PasswordResetModal",
  setup(){
    const {mobile} = useDisplay()
    const {axios} = useAxios("administration")

    return {
      mobile,
      adminEndpoint: axios as UserEndpoint
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
          <v-card
              v-bind="$attrs"
              min-height="40vh"
              max-height="60vh"
              class="d-flex flex-column"
          >
            hi
          </v-card>
        </v-col>
      </v-row>
    </v-expand-transition>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>