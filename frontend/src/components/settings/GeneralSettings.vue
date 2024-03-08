<script lang="ts">
import {defineComponent} from "vue";
import {useConfigStore} from "@/store";

export default defineComponent({
  name: "GeneralSettings",
  setup(){
    const configStore = useConfigStore();
    return {
      configStore
    }
  },
  computed:{
    languages() {
      return this.$i18n.availableLocales;
    },
    currentLanguage:{
      get(){
        return this.configStore.language
      },
      set(value: string){
        this.configStore.languageChange(value)
      }
    },
    isDefault(){
      return this.configStore.language === "default"
    }
  },
  methods:{
    defaultLanguage(){
      this.currentLanguage = 'default'
      this.$refs["language-select"].blur()
    }
  }
})
</script>

<template>
<app-settings-card
  :title="$t('settings.general.title')"
>
  <app-setting
      :title="$t('settings.general.lang')"
  >
    <v-select
      ref="language-select"
      density="compact"
      hide-details="true"
      v-model="currentLanguage"
      :items="languages"
    >
      <template #prepend-item>
        <v-list-item
            :active="isDefault"
            @click="defaultLanguage"
            title="Browser default"
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