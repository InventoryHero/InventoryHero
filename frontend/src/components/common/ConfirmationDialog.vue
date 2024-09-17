<script setup lang="ts">

const {
  title="",
  text="",
  cancelText="",
  confirmText="",
  cancelIcon="mdi-cancel",
  dialogOpened=false,
  onConfirm,
  onCancel
} = defineProps<{
  title?: string,
  text?: string,
  cancelText?: string,
  confirmText?: string,
  cancelIcon?: string,
  confirmIcon?: string,
  dialogOpened?: boolean,
  onConfirm?: () => void,
  onCancel?: () => void
}>()

</script>

<template>
  <v-dialog
      :model-value="dialogOpened"
      persistent
      no-click-animation
  >
    <v-row
      justify="center"
    >
      <v-col
        lg="6"
        cols="12"
      >
        <v-card
        >
          <template v-slot:title>
            <slot name="title">
              {{ title }}
            </slot>
          </template>
          <template v-slot:text>
            <slot name="text">
              {{ text }}
            </slot>
          </template>

          <v-card-actions
            class="overflow-auto"
          >
            <v-btn
                :prepend-icon="cancelIcon"
                :text="cancelText"
                @click="onCancel"
            />
            <v-btn
                :prepend-icon="confirmIcon"
                :text="confirmText"
                @click="onConfirm"
            />
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>