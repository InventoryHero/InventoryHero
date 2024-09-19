<script setup lang="ts">
import {useAuthStore} from "@/store";


const authStore = useAuthStore();
const {t} = useI18n()

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

const afterText = computed(() => {
  return t('households.all_displayed')
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
                <app-content-scroll-after
                  :text="afterText"
                />
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