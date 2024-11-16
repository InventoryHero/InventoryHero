<script setup lang="ts">

import {useAuthStore, useGeneralSocketStore} from "@/store";
import {computed, ref, useTemplateRef} from "vue";
import {useI18n} from "vue-i18n";
import {User} from "@/types";
import useFieldIsNotTakenValidator from "@/composables/useFieldIsNotTakenValidator.ts";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {useNotification} from "@kyvg/vue3-notification";

const {t: $t} = useI18n()

const authStore = useAuthStore()
const generalSocket = useGeneralSocketStore()
const {axios: userEndpoint} = useAxios<UserEndpoint>("user")
const {notify} = useNotification()
const {styling} = useAppStyling()

const editedData = ref<Partial<User>>({})
const isValid = ref(false)
const userForm = useTemplateRef('userForm')
const saving = ref(false)
const resetPassword = ref(false)

const {
  isTaken: usernameTaken,
  validateField: usernameNotTakenValidator
} = useFieldIsNotTakenValidator($t('administration.users.rules.username_taken'))

const {
  isTaken: emailTaken,
  validateField: emailNotTakenValidator
} = useFieldIsNotTakenValidator($t('administration.users.rules.email_taken'))

const {isValidEmailRule} = useEmailRule()
const {usernameCharacterRule} = useUserNameCharacterRule()

const notEmpty = (value: string) => !!value || $t('administration.users.rules.field_required')

const username = computed({
  get(){
    if(editedData.value.username === undefined){
      return authStore.user?.username ?? ''
    }
    return editedData.value.username
  },
  set(value: string){
    if(value === authStore.user?.username){
      editedData.value.username = undefined
      return
    }
    editedData.value.username = value
    generalSocket.isUserNameTaken(value ?? '').then((isTaken: boolean) => {
      if(value === authStore.user?.username){
        usernameTaken.value = false
        return
      }
      usernameTaken.value = isTaken
    })
  }
})
const email = computed({
  get(){
    if(editedData.value.email === undefined){
      return authStore.user?.email ?? ''
    }
    return editedData.value.email
  },
  set(value: string){
    if(value === authStore.user?.email){
      editedData.value.email = undefined
      return
    }
    editedData.value.email = value
    generalSocket.isEmailTaken(value ?? '').then((isTaken: boolean) => {
      if(value === authStore.user?.email){
        emailTaken.value = false
        return
      }
      emailTaken.value = isTaken
    })
  }
})
const firstname = computed({
  get(){
    if(editedData.value.firstName === undefined){
      return authStore.user?.firstName ?? ''
    }
    return editedData.value.firstName
  },
  set(value: string){
    if(value === authStore.user?.firstName){
      editedData.value.firstName = undefined
      return
    }
    editedData.value.firstName = value
  }
})
const lastname = computed({
  get(){
    if(editedData.value.lastName === undefined){
      return authStore.user?.lastName ?? ''
    }
    return editedData.value.lastName
  },
  set(value: string){
    if(value === authStore.user?.lastName){
      editedData.value.lastName = undefined
      return
    }
    editedData.value.lastName = value
  }
})

const edited = computed(() => {
  return (
      editedData.value.username !== undefined ||
      editedData.value.email !== undefined ||
      editedData.value.firstName !== undefined ||
      editedData.value.lastName !== undefined
  )
})

function reset(){
  editedData.value = {}
  emailTaken.value = false
  usernameTaken.value = false
}

async function saveUpdatedUserdata(){
  //@ts-expect-error couldn't figure out how to type template ref
  const {valid} = await userForm.value.validate()
  if(!valid){
    return
  }
  saving.value = true
  userEndpoint.updateMe(editedData.value).then(({success, msg, user }) => {
    saving.value = false
    if(!success){
      return
    }

    authStore.updateUser(user)
    editedData.value = {}
    notify({
      title: $t(`toasts.titles.success.${msg}`),
      text: $t(`toasts.text.success.${msg}`),
      type: "success"
    })
  })

}

onBeforeRouteLeave(() => {
  resetPassword.value = false
})

</script>

<template>
  <password-reset-modal
      v-model:active="resetPassword"
      :from-admin="false"
  />
  <v-card
      density="compact"
  >
    <v-card-title
        class="shadowed d-flex justify-space-between"
    >
      {{ $t('account.profile_card.title') }}
      <app-reset-button
        :visible="edited"
        :text="$t('administration.users.reset')"
        @click="reset"
        :disabled="saving"
      />
    </v-card-title>
    <v-card-text
        class="mt-4"
    >
      <v-form
        ref="userForm"
        v-model="isValid"
        :disabled="saving"
        @submit.prevent="(event) => event.preventDefault()"
      >
        <v-row dense>
          <v-col>
            <v-text-field
                :label="$t('account.profile_card.username')"
                v-model="username"
                :rules="[notEmpty, usernameNotTakenValidator, usernameCharacterRule]"
                v-bind="styling"
            />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col>
            <v-text-field
                :label="$t('account.profile_card.email')"
                :rules="[notEmpty, emailNotTakenValidator, isValidEmailRule]"
                v-model="email"
                v-bind="styling"
            />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col>
            <v-text-field
                :label="$t('account.profile_card.firstname')"
                :placeholder="$t('account.profile_card.firstname')"
                v-model="firstname"
                v-bind="styling"
            />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col>
            <v-text-field
                :label="$t('account.profile_card.lastname')"
                v-model="lastname"
                v-bind="styling"
            />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn
          variant="elevated"
          rounded="sm"
          density="compact"
          :text="$t('account.profile_card.change_pw')"
          color="primary"
          @click="resetPassword=true"
      />
      <v-spacer />
      <v-btn
          variant="elevated"
          rounded="sm"
          density="compact"
          :text="$t('account.profile_card.save_changes')"
          color="primary"
          :disabled="!edited || !isValid || saving"
          :loading="saving"
          @click="saveUpdatedUserdata"
      />
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss">

</style>