<script setup lang="ts">
import {HouseholdWithMemberPublic} from "@/api/types/households.ts";

const {t} = useI18n()
const {household: householdEndpoint} = useAxios()

const update = ref(false)
const households = ref([] as Array<HouseholdWithMemberPublic>)
const collapsed = ref(true)
const createHouseholdCollapsed = computed({
  get(){
    return households.value.length > 0 && collapsed.value
  },
  set(value: boolean){
    collapsed.value = value
  }
})

const afterText = computed(() => {
  return t('households.all_displayed')
})

const onLeave = (id: string) => {
  households.value = households.value.filter(h => h.id !== id)
  update.value = true
  nextTick(() => {
    update.value = false
  })
}


onMounted(async () => {
  const {success, data} = await householdEndpoint.all()
  if(success){
    households.value = data ?? []
  }
})

</script>

<template>


  <v-row
      justify="center"
  >
    <v-col
        cols="12"
        lg="8"
    >

      <create-household-card
          @created="(newHousehold: HouseholdWithMemberPublic) => households.push(newHousehold)"
          v-model:collapsed="createHouseholdCollapsed"
          class="fill-width"
      />
      <v-divider
          color="primary"
          class="mt-2 mb-2"
          thickness="2"
          opacity="25%"
      />

      <v-card
          class="flex-1-1 fill-width"
      >
        <v-card-text
            class="position-relative fill-height"
        >
          <household-card
              v-for="item in households"
              :household="item"
              @left="onLeave"
          />

        </v-card-text>

      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.create-household {
  position: sticky;
  top: calc(var(--v-layout-top) + 12px);
  z-index: 2;
}
</style>

<route>
{
  "meta": {
    "requiresAuth": true,
    "requiresHousehold": false
  }
}
</route>