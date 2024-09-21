<script setup lang="ts">
import {usePrintSettings} from "@/store";

const {t} = useI18n()
const emit = defineEmits<{
  (e: 'close'): void
}>()
const printSettingsStore = usePrintSettings()
const tab = ref<string>("configuration")

function close(){
  printSettingsStore.reset()
  emit('close')
}

</script>

<template>
  <v-card
    class="fill-height"
  >
    <v-card-title
      class="pa-0 d-flex justify-space-between align-center"
    >

      <v-tabs
          color="primary"
          v-model="tab"
          class="flex-0-0"
      >
        <v-tab
            value="configuration"
        >
          {{t('print.configuration')}}
        </v-tab>
        <v-tab
            value="preview"

        >
          {{t('print.preview')}}
        </v-tab>
      </v-tabs>
      <app-icon-btn
          icon="mdi-close"
          class="ml-2 mr-2"
          @click="close()"
      />
    </v-card-title>

    <v-card-text
      class="flex-1-1 pa-0 overflow-auto"
    >
      <v-tabs-window
          v-model="tab"
          class="fill-height"
      >
        <v-tabs-window-item
            value="configuration"
            class="fill-height"
        >
          <print-qr-code-settings />
        </v-tabs-window-item>
        <v-tabs-window-item
            value="preview"
            class="fill-height"
        >
          <print-preview />
        </v-tabs-window-item>
      </v-tabs-window>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss">

</style>