<script setup lang="ts">
import {useTemplateRef} from "vue";
import {User} from "@/types/api.ts";
import {useDisplay} from "vuetify";
import {useGeneralSocketStore} from "@/store";
import AppResetButton from "@/components/ui/AppResetButton.vue";
import useAppStyling from "@/composables/useAppStyling.ts";
import useUserNameCharacterRule from "@/composables/useUserNameCharacterRule.ts";
import useEmailRule from "@/composables/useEmailRule.ts";

const {mobile} = useDisplay()
const generalSocket = useGeneralSocketStore()
const {styling} = useAppStyling()
const {t: $t} = useI18n()

const emit = defineEmits<{
  (e: 'close'): void,
  (e: 'click:save', payload: Partial<User>): void
}>()

// user
const user = defineModel<Partial<User>>()
const updatedUserData = ref<Partial<User>>({})
const username = computed({
  get(){
    if(updatedUserData.value.username !== undefined){
      return updatedUserData.value.username
    }
    return user.value?.username ?? ''
  },
  set(newValue: string){
    updatedUserData.value.username = newValue
  }
})
const firstName = computed({
  get(){
    if(updatedUserData.value.firstName !== undefined){
      return updatedUserData.value.firstName
    }
    return user.value?.firstName ?? ''
  },
  set(newValue: string){
    updatedUserData.value.firstName = newValue
  }
})
const lastName = computed({
  get(){
    if(updatedUserData.value.lastName !== undefined){
      return updatedUserData.value.lastName
    }
    return user.value?.lastName ?? ''
  },
  set(newValue: string){
    updatedUserData.value.lastName = newValue
  }
})
const email = computed({
  get(){
    if(updatedUserData.value.email !== undefined){
      return updatedUserData.value.email
    }
    return user.value?.email ?? ''
  },
  set(newValue: string){
    updatedUserData.value.email = newValue
  }
})
const password = computed({
  get(){
    if(updatedUserData.value.password !== undefined){
      return updatedUserData.value.password
    }
    return user.value?.password ?? ''
  },
  set(newValue: string){
    updatedUserData.value.password = newValue
  }
})
const admin = computed({
  get(){
    if(updatedUserData.value.isAdmin !== undefined){
      return updatedUserData.value.isAdmin
    }
    return user.value?.isAdmin ?? ''
  },
  set(admin: boolean){
    updatedUserData.value.isAdmin = admin
  }
})


const {
  edit=false,
  loading=false,
  title=""
} = defineProps<{
  edit?: boolean,
  loading?: boolean,
  title?: string
}>()

const edited = ref(false)
const valid = ref(false)
const usernameFree = ref(true)
function checkUserName(){
  edited.value = true;
  generalSocket.isUserNameTaken(updatedUserData.value.username ?? '').then((isTaken) => {
    usernameFree.value = !isTaken
  })
}
const emailFree = ref(true)
function checkEmail(){
  edited.value = true;
  generalSocket.isEmailTaken(updatedUserData.value.email ?? '').then((isTaken) => {
    emailFree.value = !isTaken
  })
}
const rules = {
  required: (value: string) => !!value || $t('administration.users.rules.field_required'),
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  username_free: (value: string) => usernameFree.value || $t('administration.users.rules.username_taken'),
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
  email_free: (_: string) =>  emailFree.value || $t('administration.users.rules.email_taken'),
}
const {usernameCharacterRule} = useUserNameCharacterRule()
const {isValidEmailRule} = useEmailRule()

const form = useTemplateRef("form")
function reset(){
  if(loading){
    return
  }
  updatedUserData.value = {}
  if(!edit){
    //@ts-expect-error don't know how to type it
    form.value.reset()
  }
  edited.value = false
}

async function saveUser(){
  if(!edited.value){
    return
  }
  //@ts-expect-error don't know how to type it
  const {valid} = await form.value.validate()
  if(!valid){
    return
  }
  emit('click:save', updatedUserData.value)
}

function close(){
  if(loading){
    return
  }
  emit('close')
}

function setPasswordEdited(){
  edited.value = true;
}

onBeforeUnmount(() => {
  updatedUserData.value = {}
  edited.value = false
})
</script>

<template>
  <v-card
    v-bind="$attrs"
    :min-height="mobile ? '100vh' : '80vh'"
    :max-height="mobile ? '100vh' : '80vh' "
    class="d-flex flex-column"
  >
    <v-card-title
      class="d-flex align-center shadowed flex-0-0"
    >
      {{ title }}
      <v-spacer />
      <app-reset-button
          @click="reset()"
          :text="$t('administration.users.reset')"
          :visible="edited"
          :disabled="loading"
      />
      <app-icon-btn
        icon="mdi-close"
        @click="close()"
      />
    </v-card-title>
    <v-card-text
      class="mt-4 test flex-1-1 overflow-auto"
    >
      <v-form
        ref="form"
        v-model="valid"
        @submit.prevent="(event) => event.preventDefault()"
      >
        <v-row dense>
          <v-col>
            <v-text-field
                ref="usernameField"
                v-bind="styling"
                :label="$t('administration.users.username')"
                v-model="username"
                :rules="[rules.required, rules.username_free, usernameCharacterRule]"
                @update:model-value="checkUserName()"
            />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col
            lg="6"
            cols="12"
          >
            <v-text-field
                v-bind="styling"
                :label="$t('administration.users.first_name')"
                v-model="firstName"
                @update:model-value="edited = true"
                @click:clear="firstName = ''"
            />
          </v-col>
          <v-col
              lg="6"
              cols="12"
          >
            <v-text-field
                v-bind="styling"
                :label="$t('administration.users.last_name')"
                v-model="lastName"
                @update:model-value="edited = true"
                @click:clear="lastName = ''"
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            <v-text-field
                ref="emailField"
                v-bind="styling"
                :label="$t('administration.users.email')"
                v-model="email"
                :rules="[rules.required, rules.email_free, isValidEmailRule]"
                @update:model-value="checkEmail()"
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            <app-password-textfield
                v-if="!edit"
                v-bind="styling"
                :label="$t('administration.users.password')"
                v-model="password"
                :rules="[rules.required]"
                @update:model-value="setPasswordEdited()"
                class="mb-4"
            />
          </v-col>
        </v-row>
        <v-divider
            class="border-opacity-25 mb-2"
            color="primary"
            :thickness="2"
        />
        <p class="text-h5">
          {{ $t('administration.users.roles')}}
        </p>
        <v-checkbox
          :label="$t('administration.users.admin')"
          color="primary"
          v-model="admin"
          @update:model-value="edited = true"
        />
      </v-form>

    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
          prepend-icon="mdi-content-save"
          variant="elevated"
          color="primary"
          @click="saveUser()"
          :disabled="!edited || !valid"
          :loading="loading"
      >
        {{ $t('administration.users.save_user') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss">

</style>