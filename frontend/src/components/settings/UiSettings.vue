<script setup lang="ts">
import useConfigStore from '@/stores/useConfigStore'
import useAppStyling from '@/composables/useAppStyling.ts'
import { useTheme } from 'vuetify'

const configStore = useConfigStore()
const { btnStyle } = useAppStyling()
const { t } = useI18n()
const vuetifyTheme = useTheme()

const { theme, useTransitions, color } = storeToRefs(configStore)

const colorMenu = ref<boolean>(false)
const newColor = ref<string>(configStore.color)

const saveColor = () => {
  color.value = newColor.value
  colorMenu.value = false
}

watch(colorMenu, () => {
  newColor.value = configStore.color
})

watch(theme, (newTheme, oldTheme) => {
  if (newTheme !== oldTheme) {
    vuetifyTheme.change(theme.value)
  }
})
watch(color, (newColor: string, oldColor: string) => {
  if (newColor !== oldColor) {
    configStore.applyColor()
  }
})
</script>

<template>
  <app-settings-card :title="t('settings.ui.title')">
    <v-divider />
    <app-setting :title="t('settings.ui.theme.title')">
      <v-radio-group
        v-model="theme"
        inline
        hide-details
      >
        <v-spacer />
        <v-radio
          :label="t('settings.ui.theme.dark')"
          value="dark"
        ></v-radio>
        <v-radio
          :label="t('settings.ui.theme.system')"
          value="system"
        ></v-radio>
        <v-radio
          :label="t('settings.ui.theme.light')"
          value="light"
        />
      </v-radio-group>
    </app-setting>
    <v-divider />
    <app-setting :title="t('settings.ui.color')">
      <v-menu
        v-model="colorMenu"
        :close-on-content-click="false"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="{
              ...props,
              ...btnStyle
            }"
            size="small"
            :text="t('settings.ui.select_color')"
          />
        </template>
        <v-card>
          <v-color-picker
            :elevation="0"
            v-model="newColor"
          />
          <v-card-actions>
            <v-btn
              prepend-icon="mdi-close"
              @click="colorMenu = false"
              :text="t('settings.ui.close')"
            />
            <v-spacer />

            <v-btn
              v-bind="btnStyle"
              prepend-icon="mdi-content-save"
              :text="t('settings.ui.save_color')"
              @click="saveColor"
            />
          </v-card-actions>
        </v-card>
      </v-menu>
    </app-setting>
    <v-divider />
    <app-setting :title="t('settings.ui.transitions')">
      <v-switch
        class="d-inline-flex"
        color="primary"
        :hide-details="true"
        density="compact"
        v-model="useTransitions"
        @click.stop
        @click="useTransitions = !useTransitions"
      />
    </app-setting>
    <v-divider />
    <app-setting>
      <v-btn
        v-bind="btnStyle"
        size="small"
        @click="configStore.reset()"
      >
        {{ t('settings.ui.reset') }}
      </v-btn>
    </app-setting>
  </app-settings-card>
</template>

<style scoped lang="scss"></style>
