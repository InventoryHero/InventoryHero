<script setup lang="ts">

defineOptions({
  inheritAttrs: false
})

const {styling} = useAppStyling()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const text = defineModel<string>("title")
const edit = defineModel<boolean>("edit")

const editClicked = computed(() => edit.value)
console.log(edit)
const {
  disabled=false,
  editTogglesTextfield=false
} = defineProps<{
  disabled?: boolean,
  editTogglesTextfield?: boolean
}>()

const textfieldVisible = computed(() => {
  if(editTogglesTextfield){
    return editClicked.value
  }
  return false
})

const editBtnColor = computed(() => {
  if(edit.value){
    return 'primary'
  }
  return ''
})

</script>

<template>
  <v-card-title
      class="pb-0 d-flex align-center justify-space-between"
  >
    <v-text-field
        v-if="textfieldVisible"
        density="compact"
        hide-details="auto"
        v-model="text"
        v-bind="{
          ...$attrs,
          ...styling
        }"
        :disabled="disabled"
    >
    </v-text-field>
    <template v-else>
      <div
          class="d-block text-truncate"
      >
        {{ text }}
      </div>
    </template>

    <div
      class="ms-2"
    >
      <app-icon-btn
          icon="mdi-pencil"
          :color="editBtnColor"
          :disabled="disabled"
          @click="edit=true"

      />
      <app-icon-btn
          icon="mdi-close"
          :disabled="disabled"
          @click="emit('close')"
      />
    </div>

  </v-card-title>
</template>

<style scoped lang="scss">

</style>