<template>
  <template v-if="loading">
    <v-skeleton-loader
      v-if="loading"
      type="list-item-avatar-two-line"
      class="mb-4"
    />
  </template>
  <template v-else-if="mdAndUp">
    <v-data-table
      :items="users"
      :loading="loading"
    />
  </template>
  <template v-else>
    <v-list>
      <v-list-item
        v-for="user in users"
        :title="user.username"
        @click="router.push(`/administration/users/user/${user.id}`)"
      />
    </v-list>
  </template>
</template>

<script setup lang="ts">
import { UserPublic } from '@/api/types/households'
import useAxios from '@/composables/useAxios'
import { useDisplay } from 'vuetify/lib/composables/display.mjs'

const { admin: adminEndpoint } = useAxios()
const { mdAndUp } = useDisplay()
const router = useRouter()

const users = ref<UserPublic[]>([])
const loading = ref<boolean>(false)

const loadUsers = async () => {
  loading.value = true
  const { success, data, error } = await adminEndpoint.getAllUsers()
  console.log(data)
  users.value = data as UserPublic[]
  loading.value = false
}

onBeforeMount(() => {
  loadUsers()
})
</script>

<style scoped></style>

<route>
{
    "meta": {
        "layout": false
    }
}
</route>
