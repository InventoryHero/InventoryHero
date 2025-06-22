<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue'
import {CategoryReadSchema, ItemSummarySchema} from "@/api/types/items.ts";
import {onBeforeRouteUpdate} from "vue-router";
import ItemSummaryList from "@/components/items/ItemSummaryList.vue";

const {items: itemsEndpoint} = useAxios()
const { mdAndUp, xs, sm, md, lg, xl } = useDisplay()
const {textFieldStyling, btnStyle} = useAppStyling()
const route = useRoute()

const items = ref<Array<ItemSummarySchema>>([])
const categories =ref<Array<CategoryReadSchema>>([])
const loading = ref<boolean>(true)
const needle = ref<string|undefined>(undefined)
const categoryFilter = ref<Array<string>>([])



async function loadItems() {
  loading.value = true
  const {success: itemsSuccess, data, error: itemsError} = await itemsEndpoint.getAllItemsSummary()
  if(!itemsSuccess){
    // TODO NOTIFY
    console.log(itemsError)
    return
  }
  items.value = data ?? []

  const {success: categoriesSuccess, data: cats, error: categoriesError} = await itemsEndpoint.getAllCategories()
  if(!categoriesSuccess){
    // TODO NOTIFY
    console.log(categoriesError)
    return
  }
  categories.value = cats ?? []
  loading.value = false
}

const filteredItems = computed(() => {
  let filtered = items.value
  if(needle.value ){
    filtered = filtered.filter(x => x.name.toLowerCase().includes((needle.value ?? '').toLowerCase()))
  }
  if(categoryFilter.value.length > 0){
    filtered = filtered.filter(item => {
      return item.categories?.some(category => categoryFilter.value.includes(category.id))
    })
  }
  return filtered
})



onBeforeMount(() => {
  loadItems()
})
</script>

<template>

  <search-card
      :disabled="loading"
      :loading="loading"
      v-model="needle"
  >
    <v-row dense>
      <v-col>
        <v-menu
            :close-on-content-click="false"
            scroll-strategy="close"
            offset-y
            bottom
            nudge-bottom="3"
        >
          <template v-slot:activator="{props}">
            <v-btn
                v-bind="{...props, ...btnStyle}"
                prepend-icon="mdi-shape"
                size="small"
                variant="outlined"
            >
              Categories
            </v-btn>
          </template>
          <v-card
              :width="xs ? '300' : '400'"
              class="mt-2"
          >
            <v-card-text>
              <v-autocomplete
                  v-model="categoryFilter"
                  v-bind="textFieldStyling"
                  density="compact"
                  :items="categories"
                  multiple
                  item-title="name"
                  item-value="id"
              />
            </v-card-text>
          </v-card>
        </v-menu>
      </v-col>
    </v-row>
  </search-card>



  <item-summary-list
      v-if="!loading"
      v-model="filteredItems"
  />

  <!-- A simple loading indicator -->
  <div v-else class="text-center pa-16">
    <!--TODO-->
    <v-progress-circular indeterminate size="64"></v-progress-circular>
  </div>

</template>

<style scoped lang="scss">

</style>
