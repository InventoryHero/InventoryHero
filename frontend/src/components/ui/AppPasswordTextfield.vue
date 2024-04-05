<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AppPasswordTextfield",
  computed: {
    model:{
      get(){
        return this.password
      },
      set(value){
        if(value !== '')
        {
          this.visibilityIconShown=true
        }
        this.$emit('update:modelValue', value)
      }
    },
    passwordVisible(){
      return this.visible
    },
  },
  props: {
    password: {
      type: String,
      default: ''
    }
  },
  data()
  {
    return {
      visible: false,
      visibilityIconShown: false
    }
  },
  methods:{
    showPassword(){
      this.visible = !this.visible
    }
  }

})
</script>

<template>
  <v-text-field
      v-bind="$attrs"
      :type="visible ? 'text' : 'password'"
      v-model="model"
      hide-details="auto"
  >
    <template #append-inner>
      <v-icon
          @click="showPassword()"
          v-if="visibilityIconShown"
          :icon="passwordVisible ? 'fa:fas fa-eye-slash' : 'fa:fas fa-eye'"
          size="x-small"
      ></v-icon>
    </template>
  </v-text-field>
</template>

<style scoped lang="scss">

</style>