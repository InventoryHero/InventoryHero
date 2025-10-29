<script setup lang="ts">
import useConfigStore from '@/stores/useConfigStore'
import useAppStyling from '@/composables/useAppStyling.ts'
import { setI18nLanguage } from '@/plugins/i18n'

const configStore = useConfigStore()
const { selectStyling } = useAppStyling()
const { t, availableLocales } = useI18n()

const { language } = storeToRefs(configStore)

watch(language, (_) => {
  setI18nLanguage(language.value)
})
</script>

<template>
  <app-settings-card :title="t('settings.general.title')">
    <app-setting :title="t('settings.general.language')">
      <v-select
        ref="language-select"
        v-bind="selectStyling"
        density="compact"
        :clearable="false"
        v-model="language"
        :items="availableLocales"
      >
        <template #prepend-item>
          <v-list-item
            :active="language === 'default'"
            @click="language = 'default'"
            :title="t('settings.general.languages.default')"
          ></v-list-item>
        </template>
        <template v-slot:item="{ item, props }">
          <v-list-item
            v-bind="props"
            :title="t(`settings.general.languages.${item.raw}`)"
          />
        </template>
        <template v-slot:selection="{ item }">
          {{ t(`settings.general.languages.${item.raw}`) }}
        </template>
      </v-select>
    </app-setting>
    <v-divider />
  </app-settings-card>
</template>

<style scoped lang="scss"></style>
