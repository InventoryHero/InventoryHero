<script lang="ts">
import {useAuthStore} from "@/store";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {Household} from "@/types"
import HouseholdQuickSelectCard from "@/components/widgets/Households/HouseholdQuickSelectCard.vue";


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
    lg="8"
  >
    <!-- profile card -->
    <v-card
      density="compact"
    >
      <v-card-title class="shadowed">
        {{ $t('account.profile_card.title') }}
      </v-card-title>
      <v-card-text
          class="mt-4"
      >
        <v-text-field
            :label="$t('account.profile_card.username')"
            variant="outlined"
            density="compact"
            :disabled="true"
            :model-value="authData.user?.username"
        >
          <template v-slot:append>
            <font-awesome-icon :icon="['fas', 'pen']"/>
          </template>
        </v-text-field>

        <v-text-field
            :label="$t('account.profile_card.email')"
            variant="outlined"
            density="compact"
            :disabled="true"
            :model-value="authData.user?.email"
        >
          <template v-slot:append>
            <font-awesome-icon :icon="['fas', 'pen']"/>
          </template>
        </v-text-field>
      </v-card-text>
      <v-card-actions
          class="justify-space-between"
      >
        <v-btn
            variant="elevated"
            rounded="sm"
            density="compact"
            :text="$t('account.profile_card.change_pw')"
            color="primary"
        />
        <v-btn
            variant="elevated"
            rounded="sm"
            density="compact"
            :text="$t('account.profile_card.save_changes')"
            color="primary"
            :disabled="true"
        />
      </v-card-actions>
    </v-card>

    <!-- household card -->
    <household-quick-select-card />
    <v-btn
      @click="console.log(authData.permissions)"
      class="mt-10"
    >
      print permissions
    </v-btn>
  </v-col>
</v-row>
</template>

<style scoped>

</style>