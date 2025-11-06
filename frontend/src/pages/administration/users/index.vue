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
    <v-card v-if="toDelete">
      <template v-slot:title>
        <i18n-t
          keypath="administration.users.delete.title"
          tag="p"
          scope="global"
        >
          <template v-slot:user>
            <span>{{ toDelete.username }}</span>
          </template>
        </i18n-t>
      </template>
      <v-card-text
        class="fill-height text-justify"
        style="hyphens: auto"
      >
        {{ t('administration.users.delete.text') }}
      </v-card-text>
      <v-card-actions>
        <v-btn
          v-bind="btnStyle"
          color="error"
          :text="t('administration.users.delete.yes')"
          @click="deleteUser"
          prepend-icon="mdi-trash-can"
        />
        <v-spacer />
        <v-btn
          v-bind="btnStyle"
          :text="t('administration.users.delete.no')"
          @click="toDelete = undefined"
          prepend-icon="mdi-cancel"
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

  <div class="d-flex justify-end">
    <v-btn
      :text="t('administration.users.create')"
      prepend-icon="mdi-plus"
      color="primary"
      @click="createNew = true"
      variant="outlined"
      class="mt-2 mb-2"
    />
  </div>
  <v-data-table
    :items="users"
    :loading="loading"
    :headers="headers"
    :search="search"
    :mobile="!mdAndUp"
    class="table"
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
      </v-toolbar>
    </template>

    <template v-slot:item.confirmed="{ item }">
      <v-icon
        v-if="item.confirmed"
        icon="mdi-check-circle"
        color="green"
      />
      <v-icon
        v-else
        icon="mdi-close-circle"
        color="red"
        @click="resendConfirmation(item.id)"
      />
    </template>

    <template v-slot:item.admin="{ item }">
      <v-icon :icon="item.admin ? 'mdi-check-circle' : 'mdi-close-circle'" />
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
          @click="remove(item)"
        ></v-icon>
      </div>
    </template>
  </v-data-table>
</template>

<script setup lang="ts">
import { UserPublic } from '@/api/types/households'
import useAxios from '@/composables/useAxios'
import { useDisplay } from 'vuetify/lib/composables/display.mjs'
import type { DataTableHeader } from 'vuetify'
import { useNotification } from '@kyvg/vue3-notification'

definePage({
  meta: {
    requiresAuth: true,
    requiresAdmin: true,
    requiresHousehold: false,
    layout: 'admin'
  }
})

const { admin: adminEndpoint } = useAxios()
const { mdAndUp } = useDisplay()
const { t } = useI18n()
const router = useRouter()
const { btnStyle } = useAppStyling()
const { notify } = useNotification()

const users = ref<UserPublic[]>([])
const loading = ref<boolean>(false)
const createNew = ref<boolean>(false)
const toDelete = ref<UserPublic | undefined>(undefined)
const search = ref<string | undefined>()

const deleteConfirmation = computed(() => !!toDelete.value)

const headers = ref<DataTableHeader[]>([
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
    sortable: true,
    align: 'end'
  },
  {
    title: t('administration.users.user.admin'),
    key: 'admin',
    sortable: true,
    align: 'end'
  },
  {
    title: t('administration.users.user.actions'),
    key: 'actions',
    sortable: false
  }
])

const edit = (userId: string) => {
  router.push(`/administration/users/user/${userId}`)
}

const remove = (user: UserPublic) => {
  toDelete.value = user
}
const deleteUser = async () => {
  // TODO LOADING
  if (toDelete.value === undefined) {
    return
  }
  const { success } = await adminEndpoint.deleteUser(toDelete.value.id)
  if (!success) {
    toDelete.value = undefined
    return
  }
  users.value = users.value.filter((x) => x.id !== toDelete.value!.id)
  toDelete.value = undefined
}

const resendConfirmation = async (userId: string) => {
  const { success } = await adminEndpoint.resendEmailConfirmation(userId)
  if (success) {
    notify({
      title: t('administration.users.resent_confirmation'),
      type: 'success'
    })
  }
}

const loadUsers = async () => {
  loading.value = true
  const { success, data, error } = await adminEndpoint.getAllUsers()

  // TODO HANDLE ERROR / NOTIFY

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

<style scoped lang="scss">
/* https://github.com/vuetifyjs/vuetify/issues/8243#issuecomment-770313450 */
.table {
  height: calc(100dvh - 140px);
  overflow: auto;
}

/* Target Vuetify’s internal wrapper safely */
:deep(.v-data-table__wrapper) {
  overflow-x: auto; /* allow horizontal scrolling if needed */
  overflow-y: auto;
  max-height: inherit;
}
</style>
