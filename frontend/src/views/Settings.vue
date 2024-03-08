<script lang="ts">
import {defineComponent} from "vue";
import {useConfigStore} from "@/store";
import AppSetting from "@/components/ui/AppSetting.vue";
import { isMobile } from 'mobile-device-detect';
import {useDisplay} from "vuetify";
import AppThemeColorPicker from "@/components/ui/AppThemeColorPicker.vue";
import UiSettings from "@/components/settings/UiSettings.vue";
export default defineComponent({
  name: "Settings",
  components: {
    UiSettings
  },
  setup(){
    const config = useConfigStore();
    return {config}
  },
  computed: {

  },
  methods:{

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
      <general-settings />
      <ui-settings />

    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>
