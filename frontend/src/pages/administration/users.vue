<template>
  <v-data-table
    :items="users"
    :loading="loading"
  />
</template>

<script setup lang="ts">
import { UserPublic } from '@/api/types/households'

const users = ref<UserPublic[]>([])
const loading = ref<boolean>(false)

const loadUsers = async () => {
    loading.value = true;
    const {success, data, error} =
}

onBeforeMount(() => {})
</script>

<style scoped></style>

<route>
{
    "meta": {
        "layout": "admin"
    }
}
</route>
