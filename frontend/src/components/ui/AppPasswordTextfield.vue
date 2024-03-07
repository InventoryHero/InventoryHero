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
    },
    rules:{
      type: Array,
      default: []
    },
    label:{
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
      density="compact"
      variant="outlined"
      :label="label"
      :type="visible ? 'text' : 'password'"
      v-model="model"
      :rules="rules"
      hide-details="auto"
  >
    <template #append-inner>
      <v-btn
          @click="showPassword()"
          v-if="visibilityIconShown"
          :icon="passwordVisible ? 'fa:fas fa-eye-slash' : 'fa:fas fa-eye'"
          size="x-small"
      ></v-btn>
    </template>
  </v-text-field>
</template>

<style scoped lang="scss">

</style>