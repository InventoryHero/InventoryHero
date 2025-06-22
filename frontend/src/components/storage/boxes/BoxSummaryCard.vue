<script setup lang="ts">
import {BoxResponseSchema} from "@/api/types/storage.ts";

const router = useRouter()
const {t} = useI18n()
const {storage: storageEndpoint} = useAxios()

const {
  box
} = defineProps<{
  box: BoxResponseSchema
}>()

const to = computed(() => {
  return router.resolve({
    name: "BoxContentView",
    params: {
      id: box.id
    }
  } )
})



</script>

<template>
  <v-card
      max-height="140px"
      class="pl-0"
      elevation="0"
      density="compact"
      :to="to"
  >
    <template v-slot:prepend>
      <v-icon icon="mdi-package-variant" />
    </template>
    <template v-slot:title>
            <span
                class="text-truncate"
            >
              {{ box.name }}
            </span>
    </template>
    <template v-slot:subtitle>
            <span
                class="text-medium-emphasis text-overline"
            >
              {{t('boxes.box.items_quantity', box.num_items ?? 0)}}
            </span>
    </template>
  </v-card>
</template>

<style scoped lang="scss">

</style>