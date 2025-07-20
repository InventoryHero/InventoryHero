<script setup lang="ts">

import useAppStyling from "@/composables/useAppStyling.ts";

type rule = ((value: string) => string | boolean) | boolean | string

const {textFieldStyling} = useAppStyling()

const password = defineModel<string>()

const {rules=[]} = defineProps<{
  rules?: Array<rule>
}>()

const visible = ref(false)

const innerIcon = computed(() => {
  if(visible.value){
    return 'mdi-eye-off'
  }
  return 'mdi-eye'
})

function showPassword(){
  visible.value = !visible.value
}
</script>

<template>
  <v-text-field
      v-bind="{
        ...textFieldStyling,
        ...$attrs
      }"
      :type="visible ? 'text' : 'password'"
      v-model="password"
      :rules="rules"
      :append-inner-icon="innerIcon"
      @click:append-inner="showPassword"
  />
</template>

<style scoped lang="scss">

</style>