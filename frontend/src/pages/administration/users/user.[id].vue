<template>
  <v-skeleton-loader
    type="image, divider, heading"
    v-if="loading"
  />

  <template v-else>
    <!--<v-hover>
  <template v-slot:default="{isHovering, props}">
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
          cursor: isHovering ? 'pointer': undefined
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
</v-hover>-->

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
                  v-model="username"
                  :label="t('administration.user.username')"
                  :rules="usernameRules"
                  autocomplete="off"
                >
                  <template v-slot:append-inner>
                    <v-icon
                      v-if="username !== user!.username"
                      icon="mdi-refresh"
                      @click="username = user!.username"
                    />
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </template>
  <!--
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                v-model="email"
                :label="t('account.email')"
                :rules="emailRules"
              >
                <template v-slot:append-inner>
                  <v-icon
                    v-if="email !== authStore.user!.email"
                    icon="mdi-refresh"
                    @click="email = authStore.user!.email"
                  />
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                v-model="firstname"
                :label="t('account.firstname')"
              >
                <template v-slot:append-inner>
                  <v-icon
                    v-if="firstname !== authStore.user!.first_name"
                    icon="mdi-refresh"
                    @click="firstname = authStore.user!.first_name"
                  />
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                v-model="lastname"
                :label="t('account.lastname')"
              >
                <template v-slot:append-inner>
                  <v-icon
                    v-if="lastname !== authStore.user!.last_name"
                    icon="mdi-refresh"
                    @click="lastname = authStore.user!.last_name"
                  />
                </template>
              </v-text-field>
            </v-col>
          </v-row>
        </v-form>
        <div class="d-flex justify-end mt-4">
          <v-btn
            v-bind="btnStyle"
            :text="t('account.save')"
            @click="saveUpdatedUserdata"
            :disabled="!edited"
          />
        </div>

        <v-divider class="mt-4 mb-4" />

        <div class="d-flex justify-space-between align-center mb-4">
          {{ t('account.password.password') }}
          <v-btn
            v-bind="btnStyle"
            variant="outlined"
            :text="
              !passwordFormVisible
                ? t('account.password.change_password')
                : t('account.password.hide_change_password')
            "
            @click="showPasswordForm"
          />
        </div>
        <v-scroll-y-transition @after-enter="scrollToBottom">
          <v-form
            ref="passwordResetForm"
            v-if="passwordFormVisible"
          >
            <v-row>
              <v-col cols="12">
                <password-text-field
                  :label="t('account.password.current_password')"
                  v-model="currPassword"
                  :rules="passwordRules"
                />
              </v-col>
              <v-col cols="12">
                <password-text-field
                  :label="t('account.password.new_password')"
                  v-model="newPassword"
                  :rules="newPasswordRules"
                />
              </v-col>
              <v-col cols="12">
                <password-text-field
                  :label="t('account.password.new_password_repeat')"
                  v-model="newPasswordRepeat"
                  :rules="newPasswordRepeatRules"
                />
              </v-col>
            </v-row>
            <div class="d-flex justify-end mt-4 flex-wrap-reverse">
              <v-btn
                v-if="smtpEnabled"
                v-bind="btnStyle"
                variant="plain"
                :text="t('account.password.forgot_password')"
                @click="forgotPassword"
              />
              <v-btn
                v-bind="btnStyle"
                :text="t('account.password.change_password')"
                :disabled="!passwordFormValid"
                @click="updatePassword"
              />
            </div>
          </v-form>
        </v-scroll-y-transition>
      </v-col>
    </v-row>
  </v-container>
  -->
</template>

<script setup lang="ts">
import { UserPublic } from '@/api/types/households'

const { admin } = useAxios()
const { t } = useI18n()
const { textFieldStyling } = useAppStyling()

const { id } = defineProps<{
  id: string
}>()

const user = ref<UserPublic | null>(null)
const loading = ref<boolean>(false)

const username = ref<string | null>(null)
const usernameRules = ref([])

onBeforeMount(() => {
  loading.value = true
  admin.getUser(id).then(({ success, data, error }) => {
    if (!success) {
      // TODO
    }
    user.value = data!
    username.value = user.value.username
    loading.value = false
  })
})
</script>

<style scoped lang="scss"></style>

<route>
    {
        
        "props": true,
        "meta": {
            "requiresAuth": true,
            "requiresAdmin": true,
            "requiresHousehold": false, 
            "layout": false
        }
    }
</route>
