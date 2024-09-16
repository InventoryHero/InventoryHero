<script setup lang="ts">
import {Household} from "@/types";
import {useAuthStore} from "@/store";
import {HouseholdEndpoint} from "@/api/http";
import {useNotification} from "@kyvg/vue3-notification";
import {useHouseholdSocketStore} from "@/store";


const authStore = useAuthStore();
const {t: $t} = useI18n()
const {notify} = useNotification()
const households = computed(() => authStore.households)
const collapsed = ref(true)
const createHouseholdCollapsed = computed({
  get(){
    return households.value.length > 0 && collapsed.value
  },
  set(value: boolean){
    collapsed.value = value
  }
})



</script>

<template>


  <v-row
    class="fill-height"
    justify="center"
    no-gutters
  >
    <v-col
      cols="12"
      lg="8"
      class="d-flex flex-column position-relative fill-height"
    >

      <create-household-card
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
          <div
              class="wrapper"
          >
            <DynamicScroller
                ref="scroller"
                class="scroll"
                :items="households"
                :min-item-size="65"
            >
              <template v-slot="{ item, index, active}">
                <DynamicScrollerItem
                    :item="item"
                    :active="active"
                    :data-index="index"
                    :size-dependencies="[
                      item.name,
                    ]"
                >
                  <household-card
                      :household="item"
                  />
                </DynamicScrollerItem>
              </template>
              <template #after>
                <v-card
                    density="comfortable"
                    elevation="0"
                >
                  <v-card-text
                    class="d-flex justify-center align-center"
                  >
                    {{ $t('households.all_displayed') }}
                  </v-card-text>
                </v-card>
              </template>
            </DynamicScroller>
          </div>
        </v-card-text>

      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
</style>