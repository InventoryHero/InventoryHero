<template>
  <create-new-user
    v-model:active="createNew"
    @user-created="
      (user: UserPublic) => {
        users.push(user)
        createNew = false
      }
    "
  />
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
      height="100%"
      :headers="headers"
    >
      <template v-slot:top>
        <v-toolbar
          flat
          density="compact"
        >
          <v-toolbar-title>
            <v-icon
              color="medium-emphasis"
              icon="mdi-account-group"
              size="x-small"
              start
            ></v-icon>

            {{ t('administration.users.title') }}
          </v-toolbar-title>

          <v-text-field
            v-model="search"
            density="compact"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            variant="solo-filled"
            flat
            hide-details
            single-line
            class="me-2"
          />

          <v-btn
            :text="t('administration.users.create')"
            prepend-icon="mdi-plus"
            color="primary"
            @click="createNew = true"
            variant="outlined"
          />
        </v-toolbar>
      </template>
    </v-data-table>
  </template>
  <template v-else>
    <v-btn
      :text="t('administration.users.create')"
      prepend-icon="mdi-plus"
      color="primary"
      @click="createNew = true"
      class="mb-3"
    />

    <v-list>
      <v-list-item
        v-for="user in users"
        :title="user.username"
        class="mb-2 mt-2"
      >
        <template v-slot:append>
          <v-icon-btn
            icon="mdi-trash-can"
            @click.stop="console.log('delete trash')"
            class="me-2"
          />
          <v-icon-btn
            icon="mdi-chevron-right"
            @click="router.push(`/administration/users/user/${user.id}`)"
          />
        </template>
      </v-list-item>
    </v-list>
  </template>
</template>

<script setup lang="ts">
import { UserPublic } from '@/api/types/households'
import useAxios from '@/composables/useAxios'
import { useDisplay } from 'vuetify/lib/composables/display.mjs'

const { admin: adminEndpoint } = useAxios()
const { mdAndUp } = useDisplay()
const { t } = useI18n()
const router = useRouter()

const users = ref<UserPublic[]>([])
const loading = ref<boolean>(false)
const createNew = ref<boolean>(false)

const headers = ref([
  {
    title: t('administration.users.user.username'),
    key: 'username',
    sortable: true
  }
])

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
        "requiresAuth": true,
        "requiresAdmin": true,
        "requiresHousehold": false, 
        "layout": false
    }
}
</route>
