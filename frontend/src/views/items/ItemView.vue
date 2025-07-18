<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue'
import {CategoryReadSchema, ItemSummarySchema} from "@/api/types/items.ts";
import {onBeforeRouteUpdate} from "vue-router";
import ItemSummaryList from "@/components/items/ItemSummaryList.vue";
import itemAddedEventBus from "@/services/itemAddedEventBus.ts";
import useContentRefreshStore from "@/store/useContentRefreshStore.ts";

const {items: itemsEndpoint} = useAxios()
const { mdAndUp, xs, sm, md, lg, xl } = useDisplay()
const {textFieldStyling, btnStyle} = useAppStyling()
const contentRefreshStore = useContentRefreshStore()
const {t} = useI18n()

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


const clickOnBanner = () => {
  loadItems().then(() => {
  })
}


itemAddedEventBus.on((id) => {
  console.log(id)
  contentRefreshStore.showBanner({
    title: t('items.content_changed_title'),
    subtitle: t('items.content_changed_subtitle'),
    callback: clickOnBanner
  })
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
      :num-items="items.length"
  />

  <!-- A simple loading indicator -->
  <v-skeleton-loader
      v-else
      :loading="loading"
      type="list-item-avatar-three-line@4"
  />

</template>

<style scoped lang="scss">

</style>
