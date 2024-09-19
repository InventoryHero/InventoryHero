<script lang="ts">
import {defineComponent} from "vue";
import {useConfigStore} from "@/store";
import UiSettings from "@/components/widgets/settings/UiSettings.vue";
import GeneralSettings from "@/components/widgets/settings/GeneralSettings.vue";
export default defineComponent({
  name: "Settings",
  components: {
    UiSettings, GeneralSettings
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
    class="fill-height"
    dense
    justify="center"
  >
    <v-col
      cols="12"
      lg="8"
    >
      <general-settings />
      <ui-settings />

    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>
