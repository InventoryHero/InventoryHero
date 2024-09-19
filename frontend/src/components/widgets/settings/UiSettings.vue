<script setup lang="ts">

import {useConfigStore} from "@/store";

const configStore = useConfigStore()
const {mobile} = useDisplay()

const theme = computed(() => configStore.theme)
function changeTheme(){
  configStore.themeChange({
    dark: !theme.value
  })
}

const dock = computed(() => configStore.dock)
function useDock(){
  configStore.toggleDock(!dock.value)
}

const transitions = computed(() => configStore.transitions)
function toggleTransitions(){
  configStore.toggleTransitions(!transitions.value)
}

function reset(){
  configStore.reset()
}
/*export default defineComponent({
  name: "UiSettings",
  setup(){
    const config = useConfigStore();
    return {config}
  },
  computed: {
    theme(){
      return this.config.theme
    },
    dock(){
      return this.config.dock
    },
    mobile(){
      return this.$vuetify.display.mobile
    },
  },
  methods:{
    changeTheme(){
      this.config.themeChange({
        dark: !this.theme
      } )
    },
    reset(){
      this.config.reset();
    },
    useDock(){
      this.config.toggleDock(!this.dock)
    },
  }
})*/
</script>

<template>
  <app-settings-card
    :title="$t('settings.ui.title')"

  >
    <app-setting
        :title="$t('settings.ui.preset')"
    >
    </app-setting>
    <v-divider/>
    <app-setting
        :title="$t('settings.ui.theme')"
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
        :title="$t('settings.ui.color')"
    >
      <app-theme-color-picker
          :title="$t('settings.ui.select_color')"

      />
    </app-setting>
    <v-divider/>
    <template v-if="mobile">
      <app-setting
          :title="$t('settings.ui.use_dock')"

      >
        <v-switch
            class="d-inline-flex"
            color="primary"
            :hide-details="true"
            density="compact"
            v-model="dock"
            @click.stop
            @click="useDock"
        />
      </app-setting>
      <v-divider/>
    </template>
    <app-setting
        :title="$t('settings.ui.transitions')"
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
          variant="outlined"
          size="small"
          color="primary"
          class="me-1"
          @click="reset()"
      >
        {{ $t('settings.ui.reset') }}
      </v-btn>
    </app-setting>
  </app-settings-card>


</template>

<style scoped lang="scss">

</style>