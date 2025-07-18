<script setup lang="ts">
import {ItemSummarySchema} from "@/api/types/items.ts";

const {t} = useI18n()
const router = useRouter()

const {
  item,
  height = "140px",
  from
} = defineProps<{
  item: ItemSummarySchema
  height?: string|number,
  from?: string
}>()

const hasImage = computed(() => {
  return false
})

const iconPlaceholder = computed(() => {
  return item.name.toUpperCase()[0]
})

const to = computed(() => {
  return router.resolve({
    name: "/items/[id]",
    params: {
      id: item.id
    },
    query: {
      fromStorage: from
    }
  })
})


</script>

<template>
  <v-card
    :to="to"
  >
    <v-row
        dense
    >
      <v-col
          cols="4"
      >
        <v-img
            v-if="hasImage"
            :height="height"
            src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
            cover
        >

        </v-img>
        <v-sheet
            v-else
            :height="height"
            class="d-flex justify-center align-center text-h5 text-disabled"
        >
          {{iconPlaceholder}}
        </v-sheet>



      </v-col>

      <v-col
          cols="8"
      >
        <v-card
          :max-height="height"
          class="pl-0"
          elevation="0"
          density="compact"
        >

          <template v-slot:title>
            <span
              class="text-truncate"
            >
              {{ item.name }}
            </span>
          </template>
          <template v-slot:subtitle>
            <category-chip
                v-for="category in item.categories"
                :category="category"
                density="compact"
                size="small"
                :text="category.name"
                variant="tonal"
                color="primary"
                class="me-1"
            />
          </template>
          <template v-slot:append>
            <span
                class="text-medium-emphasis text-overline pl-1 pr-1"
            >
              {{t('items.quantity', {quantity: item.total_quantity})}}
            </span>
          </template>
          <v-card-text class="pt-1 multi-line-truncate text-medium-emphasis">
            {{ item.description }}
          </v-card-text>


        </v-card>

      </v-col>
    </v-row>
  </v-card>
</template>

<style scoped lang="scss">
:deep(.v-card-item){
  margin-bottom: 0 !important;
  padding-bottom: 0 !important;
}

.multi-line-truncate {
  display: -webkit-box;
  -webkit-line-clamp: 3; /* Change to desired number of lines */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.5em;
  max-height: calc(1.5em * 3);
}
</style>