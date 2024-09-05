<script setup lang="ts">
import {ref} from "vue";
defineOptions({
  inheritAttrs: false
})
const emit = defineEmits<{
  (e: 'refuse'): void,
  (e: 'consent'): void
}>()

const props = defineProps<{
  title?: string,
  body?: string,
  btnText?: string,
  confirmText?: string,
  refuseText?: string,
}>()

const visible = ref(false)

function accept(){
  emit("consent")
  visible.value = false

}
function deny(){
  emit("refuse")
  visible.value = false
}

</script>

<template>
<v-dialog
  v-model="visible"
  persistent
  max-width="500"
  max-height="500"
>
  <v-card
    max-height="500"
  >
    <v-card-title
        class="shadowed"
    >
      {{ props.title ?? 'Confirm' }}
    </v-card-title>
    <v-card-text
      class="overflow-auto"
    >
      {{ props.body ?? ''}}
    </v-card-text>
    <v-card-actions
      class="d-flex justify-space-between"
    >
      <slot name="actions"
        :accept="accept"
        :deny="deny"
      >
        <v-btn
            variant="elevated"
            color="grey"
            @click="deny"
            class="me-4"
        >
          {{ props.refuseText ?? 'deny' }}
        </v-btn>
        <v-btn
            variant="elevated"
            color="grey"
            @click="accept"
        >
          {{ props.confirmText ?? 'accept' }}
        </v-btn>
      </slot>
    </v-card-actions>
  </v-card>
</v-dialog>
<v-btn
  @click="visible=true"
  :disabled="visible"
  v-bind="$attrs"
>
</v-btn>
</template>

<style scoped lang="scss">

</style>