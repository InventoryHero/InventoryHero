<script setup lang="ts">
import {useConfigStore} from "@/store";
import useAppStyling from "@/composables/useAppStyling.ts";

const configStore = useConfigStore()
const {selectStyling} = useAppStyling()
const {t, availableLocales} = useI18n()



const locales = computed(() => {
  return availableLocales.map((value) => {
    return {
      key: value,
      title: t(`settings.general.languages.${value}`)
    }
  })
})

const currentLocale = computed({
  get() {
    if(configStore.language === "default"){
      return {
        key: "default",
        title: t(`settings.general.languages.default_short`)
      }
    }

    return configStore.language
  },
  set(locale: string){
    configStore.languageChange(locale)
  }
})


</script>

<template>
<app-settings-card
  :title="t('settings.general.title')"
>
  <app-setting
      :title="t('settings.general.language')"
  >
    <v-select
      ref="language-select"
      v-bind="selectStyling"
      density="compact"
      :clearable="false"
      v-model="currentLocale"
      :items="locales"
      item-title="title"
      item-value="key"
    >
      <template #prepend-item>
        <v-list-item
            :active="configStore.language === 'default'"
            @click="currentLocale = 'default'"
            :title="t('settings.general.languages.default')"
        >
        </v-list-item>
      </template>
    </v-select>
  </app-setting>
  <v-divider/>
</app-settings-card>
</template>

<style scoped lang="scss">

</style>