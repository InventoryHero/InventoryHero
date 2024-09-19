<script lang="ts">
import {useAuthStore} from "@/store";
import HouseholdQuickSelectCard from "@/components/widgets/Households/Card/HouseholdQuickSelectCard.vue";


export default{
  components: {HouseholdQuickSelectCard},
  setup(){
    const authData = useAuthStore();
    return {authData}
  },

}
</script>

<template>
  <v-row
      justify="center"
      dense
      class="fill-width"
  >
    <v-col
        cols="12"
        md="10"
        lg="8"
    >
      <profile-card />

    </v-col>
  </v-row>
  <v-row
      class="fill-width"
      justify="center"
      dense
  >
    <v-col
        cols="12"
        md="10"
        lg="8"
    >
      <household-quick-select-card />
    </v-col>
  </v-row>

</template>

<style scoped>

</style>