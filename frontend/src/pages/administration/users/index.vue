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

  <v-dialog
    v-model="deleteConfirmation"
    persistent
    width="600px"
    height="350px"
    no-click-animation
  >
    <v-card :title="t('administration.users.user.delete.title')">
      <v-card-text class="fill-height">
        {{ t('administration.users.user.delete.text') }}
      </v-card-text>
      <v-card-actions>
        <v-btn
          :text="t('administration.users.user.delete.yes')"
          @click="deleteUser"
        />
        <v-btn
          :text="t('administration.users.user.delete.no')"
          @click="toDelete = undefined"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>

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

      <template v-slot:item.actions="{ item }">
        <div class="d-flex ga-2 justify-end">
          <v-icon
            color="medium-emphasis"
            icon="mdi-pencil"
            size="small"
            @click="edit(item.id)"
          ></v-icon>

          <v-icon
            color="medium-emphasis"
            icon="mdi-delete"
            size="small"
            @click="remove(item.id)"
          ></v-icon>
        </div>
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
import { useEventListener } from '@vueuse/core'
import { useDisplay } from 'vuetify/lib/composables/display.mjs'

const { admin: adminEndpoint } = useAxios()
const { mdAndUp } = useDisplay()
const { t } = useI18n()
const router = useRouter()

const users = ref<UserPublic[]>([])
const loading = ref<boolean>(false)
const createNew = ref<boolean>(false)
const toDelete = ref<string | undefined>(undefined)

const deleteConfirmation = computed(() => !!toDelete.value)

const headers = ref([
  {
    title: t('administration.users.user.username'),
    key: 'username',
    sortable: true
  },
  {
    title: t('administration.users.user.email'),
    key: 'email',
    sortable: true
  },
  {
    title: t('administration.users.user.first_name'),
    key: 'firstName',
    sortable: false
  },
  {
    title: t('administration.users.user.last_name'),
    key: 'lastName',
    sortable: false
  },
  {
    title: t('administration.users.user.confirmed'),
    key: 'confirmed',
    sortable: true
  },
  {
    title: t('administration.users.user.actions'),
    key: 'actions',
    sortable: false,
    align: 'end'
  }
])

const edit = (userId: string) => {
  router.push(`/administration/users/user/${userId}`)
}

const remove = (userId: string) => {
  toDelete.value = userId
}
const deleteUser = async () => {
  // TODO LOADING
  if (!toDelete.value) {
    return
  }
  const { success, error } = await adminEndpoint.deleteUser(toDelete.value!)
  if (!success) {
    // TODO
    return
  }
  users.value = users.value.filter((x) => x.id !== toDelete.value)
  toDelete.value = undefined
}

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

onBeforeRouteLeave((_to, _from, next) => {
  if (deleteConfirmation.value) {
    next(false)
    // const result = confirm('There are some unsaved changes. Discard?')
    // next(result)
    return
  }
  next()
})

/*onBeforeRouteLeave(() => {
  if (deleteConfirmation.value) {
    return false
  }
})*/
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
