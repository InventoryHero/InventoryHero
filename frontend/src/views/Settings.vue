<script lang="ts">
import {defineComponent} from "vue";
import {useConfigStore} from "@/store";
import AppSetting from "@/components/ui/AppSetting.vue";
import { isMobile } from 'mobile-device-detect';
import {useDisplay} from "vuetify";
import AppThemeColorPicker from "@/components/ui/AppThemeColorPicker.vue";
export default defineComponent({
  name: "Settings",
  components: {
    AppSetting, AppThemeColorPicker
  },
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
    }
  },
  methods:{
    isMobile() {
      return isMobile
    },
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
    }
  }
})
</script>

<template>
  <v-row
    :no-gutters="true"
    justify="center"
  >
    <v-col
      cols="12"
      lg="6"
    >
      <div
        class="text-subtitle-2 ms-4 pb-2"
      >
        {{ $t('settings.ui.title')}}
      </div>
      <v-card
        :elevation="5"
        density="compact"
        class="mb-4"
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
      </v-card>

    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.settings-header{

}
</style>
