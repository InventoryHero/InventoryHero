<script setup lang="ts">

import {useConfigStore} from "@/store";
import useAppStyling from "@/composables/useAppStyling.ts"

const configStore = useConfigStore()
const {btnStyle} = useAppStyling()
const {t} = useI18n()

const theme = computed(() => configStore.theme)
function changeTheme(){
  configStore.themeChange({
    dark: !theme.value
  })
}

const colorMenu = ref<boolean>(false)
const newColor = ref<string>(configStore.color)
const resetColor = () => {
  newColor.value = configStore.color
}
const saveColor = () => {
  configStore.themeChange({
    color: newColor.value
  })
  colorMenu.value = false
}



const transitions = computed(() => configStore.transitions)
function toggleTransitions(){
  configStore.toggleTransitions(!transitions.value)
}

function reset(){
  configStore.reset()
}

watch(colorMenu, () => {
  resetColor()
})

</script>

<template>
  <app-settings-card
    :title="t('settings.ui.title')"

  >
    <app-setting
        :title="t('settings.ui.preset')"
    >
    </app-setting>
    <v-divider/>
    <app-setting
        :title="t('settings.ui.theme')"
    >
      <v-switch
          class="d-inline-flex"
          color="primary"
          :hide-details="true"
          density="compact"
          v-model="theme"
          @click.stop
          @click="changeTheme"
      />
    </app-setting>
    <v-divider/>
    <app-setting
        :title="t('settings.ui.color')"
    >
      <v-menu
        v-model="colorMenu"
        :close-on-content-click="false"
      >
        <template v-slot:activator="{props}">
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
            <v-spacer />
            <v-btn
              v-bind="btnStyle"
              :text="t('settings.ui.save_color')"
              @click="saveColor"

            />
          </v-card-actions>
        </v-card>

      </v-menu>
    </app-setting>
    <v-divider/>
    <app-setting
        :title="t('settings.ui.transitions')"
    >
      <v-switch
          class="d-inline-flex"
          color="primary"
          :hide-details="true"
          density="compact"
          v-model="transitions"
          @click.stop
          @click="toggleTransitions"
      />
    </app-setting>
    <v-divider/>
    <app-setting
    >
      <v-btn
          v-bind="btnStyle"
          size="small"
          @click="reset()"
      >
        {{ t('settings.ui.reset') }}
      </v-btn>
    </app-setting>
  </app-settings-card>


</template>

<style scoped lang="scss">

</style>