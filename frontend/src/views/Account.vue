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
  :no-gutters="true"
>
  <v-col
    cols="12"
    md="10"
    lg="6"
  >
    <profile-card />

    <!-- household card -->
    <household-quick-select-card />

  </v-col>
</v-row>
</template>

<style scoped>

</style>