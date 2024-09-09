<script lang="ts">
import {defineComponent} from "vue";
import {useConfigStore} from "@/store";

export default defineComponent({
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
    transitions(){
      return this.config.transitions
    }
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
    toggleTransitions(){
      this.config.toggleTransitions()
    }
  }
})
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
        :title="$t('settings.ui.transitions')"
    >
      <v-switch
          class="d-inline-flex"
          color="primary"
          :hide-details="true"
          density="compact"
          v-model="transitions"
          @click.native.stop
          @click="toggleTransitions"
      />
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
          @click.native.stop
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
    <app-setting
        :title="$t('settings.ui.use_dock')"
        v-if="mobile"
    >
      <v-switch
          class="d-inline-flex"
          color="primary"
          :hide-details="true"
          density="compact"
          v-model="dock"
          @click.native.stop
          @click="useDock"
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