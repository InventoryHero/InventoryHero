<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useAxios.ts";
import {HouseholdEndpoint} from "@/api/http";
import {Household} from "@/types";

export default defineComponent({
  name: "HouseholdQuickSelectCard",
  setup(){
    const authData = useAuthStore();
    const {axios} = useNewAxios("household");
    return {axios: axios as HouseholdEndpoint, authData}
  },
  props: {
    collapsible: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    icon(){
      if(!this.collapsed){
        return 'fa:fas fa-caret-up'
      }
      return 'fa:fas fa-caret-down'
    },
    noDataText(){
      if(this.loadingUserHouseholds){
        return this.$t('account.household_card.loading_households')
      }
      return this.$t('account.household_card.create_new_household')
    },
    placeholderText(){
      if(this.loadingUserHouseholds){
        return this.$t('account.household_card.loading_households')
      } else if(this.userHouseholds.length === 0){
        return this.$t('account.household_card.create_new_household')
      }
      return this.$t('account.household_card.select_household')
    }
  },
  data(){
    return {
      loadingUserHouseholds: true,
      selectedHousehold: undefined as undefined|Household,
      userHouseholds: [] as Array<Household>,
      collapsed: false
    }
  },
  methods: {
    saveHouseholdChanges(){
      this.authData.changeHousehold(this.selectedHousehold)
      this.sortUserHouseholds()
    },
    editHouseholds(){
      this.$router.push("/households")
    },
    sortUserHouseholds()
    {
      let i = 0
      for(; i < this.userHouseholds.length; i++) {
        if (this.userHouseholds[i].id === this.authData.user?.household.id) {
          break
        }
      }
      return i
    }
  },
  async mounted() {
    this.userHouseholds = (await this.axios.getHouseholds()) as Array<Household>
    if(this.userHouseholds.length > 0)
    {
      //let selected = this.sortUserHouseholds()
      let selected = this.userHouseholds.map(e => e.id).indexOf(this.authData.user?.household?.id)
      if(selected < this.userHouseholds.length)
      {
        this.selectedHousehold = this.userHouseholds[selected]
      }

    }
    this.loadingUserHouseholds = false;
  }
})
</script>

<template>
  <v-card
      class="mt-4"
      v-bind="$attrs"
      density="compact"

  >
    <v-card-title
        class="d-flex justify-space-between align-center"
        :class="{
          shadowed: !collapsed
        }"
    >
      {{ $t('account.household_card.title') }}
      <v-btn
          v-if="collapsible"
          density="compact"
          :icon="icon"
          variant="flat"
          size="small"
          @click="collapsed = !collapsed"
      >
      </v-btn>
    </v-card-title>

    <v-slide-y-transition :group="true">
      <v-card-text
          v-if="!collapsed"
          class="mt-4"
      >
        <v-select
            :items="userHouseholds"
            :chips="true"
            item-title="name"
            hide-details="auto"
            :single-line="true"
            :placeholder="placeholderText"
            :no-data-text="noDataText"
            return-object
            v-model="selectedHousehold"
            density="compact"
            color="primary"
        >
          <template #loader>
            <v-progress-linear
                :active="loadingUserHouseholds"
                :indeterminate="true"
            />
          </template>
        </v-select>


      </v-card-text>
      <v-card-actions
          v-if="!collapsed"
          class="justify-space-between"
      >
        <v-btn
            variant="elevated"
            density="compact"
            rounded="sm"
            :text="$t('account.household_card.edit_households')"
            color="primary"
            @click="editHouseholds"
        />
        <v-btn
            variant="elevated"
            density="compact"
            rounded="sm"
            :text="$t('account.household_card.save_changes')"
            color="primary"
            :disabled="selectedHousehold === userHouseholds[0]"
            @click="saveHouseholdChanges"
        />
      </v-card-actions>
    </v-slide-y-transition>
  </v-card>
</template>

<style scoped lang="scss">

</style>