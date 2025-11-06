<template>
  <v-skeleton-loader
    type="image, divider, heading"
    v-if="loading"
  />

  <template v-else>
    <v-dialog
      v-model="passwordResetDialog"
      :max-height="mdAndUp ? '700px' : '100%'"
      :width="mdAndUp ? '600px' : '100%'"
      persistent
      no-click-animation
    >
      <v-card>
        <template v-slot:append>
          <v-icon-btn
            icon="mdi-close"
            @click="passwordResetDialog = false"
          />
        </template>
        <template v-slot:title>
          {{ t('administration.users.user.password_reset_title') }}
        </template>

        <v-card-text>
          <v-text-field
            v-bind="textFieldStyling"
            v-model="passwordResetCode"
            :clearable="false"
            :persistent-clear="false"
            readonly
          />
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            prepend-icon="mdi-clipboard"
            :text="t('administration.users.user.copy_link_to_clipboard')"
            @click="copyToClipboard"
          />
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-breadcrumbs :items="breadcrumbs">
      <template v-slot:divider>
        <v-icon icon="mdi-chevron-right"></v-icon>
      </template>
    </v-breadcrumbs>
    <v-hover>
      <template v-slot:default="{ isHovering, props }">
        <v-img
          v-bind="props"
          class="mx-auto mt-4"
          rounded="circle position-relative"
          aspect-ratio="1/1"
          height="100"
          width="100"
          cover
          :lazy-src="lazySrc"
          alt="avatar"
          :src="profilePictureSrc"
          @click="uploadProfilePicture"
          :style="{
            cursor: isHovering ? 'pointer' : undefined
          }"
        >
          <template v-slot:default>
            <v-overlay
              :model-value="!!isHovering"
              contained
              class="align-center justify-center"
              scrim="#000000"
            >
              <v-icon
                icon="mdi-camera"
                size="large"
              />
            </v-overlay>
          </template>
        </v-img>
      </template>
    </v-hover>

    <v-container class="mt-4 mb-4">
      <v-row justify="center">
        <v-col
          lg="6"
          cols="12"
        >
          <v-form
            ref="userForm"
            @submit.prevent=""
          >
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-bind="textFieldStyling"
                  :model-value="user?.username"
                  :label="t('administration.users.user.username')"
                  autocomplete="off"
                  disabled
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-bind="textFieldStyling"
                  :model-value="user?.email"
                  :label="t('administration.users.user.email')"
                  disabled
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-bind="textFieldStyling"
                  v-model="firstname"
                  :label="t('administration.users.user.firstname')"
                >
                  <template v-slot:append-inner>
                    <v-icon
                      v-if="firstnameChanged"
                      icon="mdi-refresh"
                      @click="firstname = user!.first_name"
                    />
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-bind="textFieldStyling"
                  v-model="lastname"
                  :label="t('administration.users.user.lastname')"
                >
                  <template v-slot:append-inner>
                    <v-icon
                      v-if="lastnameChanged"
                      icon="mdi-refresh"
                      @click="lastname = user!.last_name"
                    />
                  </template>
                </v-text-field>
              </v-col>
              <v-col>
                <v-checkbox
                  v-model="isAdmin"
                  :label="t('administration.users.user.is_admin')"
                />
              </v-col>
            </v-row>
          </v-form>
          <div class="d-flex justify-end mt-4">
            <v-btn
              v-bind="btnStyle"
              color="error"
              :text="t('administration.users.user.reset_password')"
              @click="resetPassword"
              class="me-2"
            />
            <v-btn
              v-bind="btnStyle"
              :text="t('administration.users.user.save')"
              @click="saveUpdatedUserdata"
              :disabled="!edited"
            />
          </div>
        </v-col>
      </v-row>
    </v-container>
  </template>
  <v-snackbar
    :timeout="5000"
    color="success"
    rounded="pill"
    v-model="copied"
    class="pb-4 ps-4 pe-4"
    @click="copied = false"
  >
    <div class="text-subtitle-1 text-center">
      {{ t('administration.users.user.copied_reset_link') }}
    </div>
  </v-snackbar>
</template>

<script setup lang="ts">
import { UserPublic } from '@/api/types/households'
import { AdminUserUpdate } from '@/api/types/user'
import router from '@/router'
import useConfigStore from '@/stores/useConfigStore'
import { BreadcrumbItem } from 'vuetify/lib/components/VBreadcrumbs/VBreadcrumbs.mjs'

definePage({
  props: true,
  meta: {
    requiresAuth: true,
    requiresAdmin: true,
    requiresHousehold: false,
    layout: 'admin'
  }
})

const { admin } = useAxios()
const { t } = useI18n()
const { textFieldStyling, btnStyle } = useAppStyling()
const route = useRoute()
const configStore = useConfigStore()
const { mdAndUp } = useDisplay()

const { id } = defineProps<{
  id: string
}>()

const { smtpEnabled } = storeToRefs(configStore)

const user = ref<UserPublic | null | undefined>(null)
const loading = ref<boolean>(false)

const firstname = ref<string | null | undefined>(null)
const lastname = ref<string | null | undefined>(null)

const isAdmin = ref<boolean>(false)

const passwordResetCode = ref<string | undefined>(undefined)

const copied = ref<boolean>(false)

const breadcrumbs = computed(() => {
  return [
    {
      title: t('administration.users.user.breadcrumbs.users'),
      to: '/administration/users',
      disabled: false
    },
    {
      title: user.value?.username,
      to: route.fullPath,
      disabled: true
    }
  ] as BreadcrumbItem[]
})

const edited = computed(() => {
  return firstnameChanged.value || lastnameChanged.value || adminChanged.value
})

const firstnameChanged = computed(
  () => user.value?.first_name !== firstname.value
)
const lastnameChanged = computed(() => user.value?.last_name !== lastname.value)
const adminChanged = computed(() => user.value?.admin !== isAdmin.value)

const lazySrc = computed(
  () =>
    `https://api.dicebear.com/8.x/bottts-neutral/svg?seed=${user.value?.username}`
)
const profilePictureSrc = computed(() => lazySrc.value)

const passwordResetDialog = computed({
  get: () => passwordResetCode.value !== undefined,
  set: (value: boolean) => {
    passwordResetCode.value = undefined
  }
})

const resetPassword = async () => {
  const { success, data, error } = await admin.resetUserPassword(user.value!.id)

  if (!success) {
    return
  }
  passwordResetCode.value = data!
}

const copyToClipboard = () => {
  navigator.clipboard
    .writeText(passwordResetCode.value)
    .then(() => {
      // e.g. show snackbar feedback
      copied.value = true
    })
    .catch(() => {})
}

const resetUser = () => {
  firstname.value = user.value?.first_name
  lastname.value = user.value?.last_name
  isAdmin.value = user.value?.admin ?? false
}

const saveUpdatedUserdata = async () => {
  const to_update = {
    first_name: firstnameChanged.value ? firstname.value : undefined,
    last_name: lastnameChanged.value ? lastname.value : undefined,
    admin: adminChanged.value ? isAdmin.value : undefined
  } as AdminUserUpdate

  const { success, data, error } = await admin.updateUser(
    user.value?.id!,
    to_update
  )

  if (!success) {
    return
  }
  user.value = data!
  resetUser()
}

onBeforeMount(() => {
  loading.value = true
  admin.getUser(id).then(({ success, data, error }) => {
    if (!success) {
      router.push('/administration/users')
      return
    }
    user.value = data!
    resetUser()
    loading.value = false
  })
})
</script>

<style scoped lang="scss"></style>
