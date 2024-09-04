<script lang="ts">
import {defineComponent, PropType} from "vue";
import {User} from "@/types/api.ts";
import {useDisplay} from "vuetify";
import {useGeneralSocketStore, useHouseholdSocket} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";


// flags for required data types
const USERNAME_SET = 1
const PASSWORD_SET = 2
const EMAIL_SET = 4



export default defineComponent({
  name: "UserCard",
  setup(){
    const {mobile} = useDisplay()
    const sockets = useHouseholdSocket()
    const generalSocket = useGeneralSocketStore()
    const {axios} = useAxios("user")


    return {
      mobile,
      sockets,
      userEndpoint: axios as UserEndpoint,
      generalSocket
    }
  },
  emits:{
    close(){
      return true
    },
    'click:save'(_: Partial<User>){
      return true;
    }
  },
  computed:{
    user() {
      return this.modelValue
    },
    username:{
      get(){
        if(this.updatedUserData.username !== undefined){
          return this.updatedUserData.username
        }
        return this.user?.username ?? ''
      },
      set(newName: string){
        this.updatedUserData.username = newName
      }
    },
    firstname: {
      get(){
        if(this.updatedUserData.first_name !== undefined){
          return this.updatedUserData.first_name
        }
        return this.user?.first_name ?? ''
      },
      set(firstname: string){
        this.updatedUserData.first_name = firstname
      }
    },
    lastname:{
      get(){
        if(this.updatedUserData.last_name !== undefined){
          return this.updatedUserData.last_name
        }
        return this.user?.last_name ?? ''
      },
      set(lastname: string){
        this.updatedUserData.last_name = lastname
      }
    },
    email:{
      get(){
        if(this.updatedUserData.email !== undefined){
          return this.updatedUserData.email
        }
        return this.user?.email ?? ''
      },
      set(newEmail: string){
        this.updatedUserData.email = newEmail
      }
    },
    password: {
      get(){
        return this.updatedUserData.password ?? ''
      },
      set(newPassword: string){
        this.updatedUserData.password = newPassword
      }
    },
    admin:{
      get(){
        if(this.updatedUserData.is_admin !== undefined){
          return this.updatedUserData.is_admin
        }
        return this.user?.is_admin ?? false
      },
      set(admin: boolean){
        this.updatedUserData.is_admin = admin
      }
    },
    textFieldStyle(){
      return {
        variant: "solo-filled",
        rounded: "lg",
        color: "primary",
        clearable: true,
        persistentClear: true,
        hideDetails: "auto",
        class: "mb-4",
        disabled: this.loading
      } as Partial<{}>
    },
    userCorrect(){
      return (PASSWORD_SET|USERNAME_SET|EMAIL_SET)
    }

  },
  props: {
    modelValue: {
      type: Object as PropType<Partial<User>>,
      default: undefined
    },
    edit: {
      type: Boolean,
      default: true
    },
    loading:{
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    }
  },
  data(){
    return {
      edited: false,
      correct: 0,
      updatedUserData: {} as Partial<User>,
      usernameFree: true,
      emailFree: true,
      rules: {
        required: (value: string) => !!value || this.$t('administration.users.rules.field_required'),
        username_free: (_: string) => this.usernameFree || this.$t('administration.users.rules.username_taken'),
        email_free: (_: string) => this.emailFree || this.$t('administration.users.rules.email_taken')
      }
    }
  },
  methods:{
    reset(){
      if(this.loading){
        return
      }
      this.updatedUserData = {}
      if(!this.edit){
        (this.$refs.form as HTMLFormElement).reset()
      }
      this.edited = false
    },
    async saveUser(){
      if(!this.edited){
        return
      }
      const {valid} = await (this.$refs.form as HTMLFormElement).validate()
      if(!valid){
        return
      }
      this.$emit('click:save', this.updatedUserData)
    },
    checkUserName(){
      this.edited = true;
      let callback = (isTaken: boolean) => {
        this.usernameFree = !isTaken

        //@ts-expect-error
        this.$refs?.usernameField?.validate()?.then((obj: Proxy<Array>) => {
          // no errors in the verification array
          this.correct &= ~USERNAME_SET;
          if(obj.length === 0){
            this.correct |= USERNAME_SET;
          }
        })
      }
      this.generalSocket.isUserNameFree(this.updatedUserData.username ?? '', callback)
    },
    checkEmail(){
      this.edited = true;
      let callback = (isTaken: boolean) => {
        this.emailFree = !isTaken
        //@ts-expect-error
        this.$refs?.emailField?.validate()?.then((obj: Proxy<Array>) => {
          // no errors in the verification array
          this.correct &= ~EMAIL_SET;
          if(obj.length === 0){
            this.correct |= EMAIL_SET;
          }
        })
      }
      this.generalSocket.isEmailFree(this.updatedUserData.email ?? '', callback)
    },
    setPasswordEdited(){
      this.edited = true;
      this.correct |= PASSWORD_SET;
    },
    close(){
      if(this.loading){
        return
      }
      this.$emit('close')
    }
  },
  unmounted() {
    this.updatedUserData = {}
    this.edited = false
  },
  beforeMount(){
    if(this.edit){
      this.correct |= (PASSWORD_SET|USERNAME_SET|EMAIL_SET);
    }
  }
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
      <v-fade-transition>
        <v-btn
            v-if="edited"
            class="me-4"
            density="comfortable"
            prepend-icon="mdi-lock-reset"
            variant="tonal"
            :disabled="loading"
            @click="reset()"
        >
          {{ $t('administration.users.reset') }}
        </v-btn>
      </v-fade-transition>
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

      >
        <v-text-field
            ref="usernameField"
            v-bind="textFieldStyle"
            :label="$t('administration.users.username')"
            v-model="username"
            :rules="[rules.required, rules.username_free]"
            @update:model-value="checkUserName()"
        />
        <v-row
            :dense="true"
            :no-gutters="mobile"
        >
          <v-col
            lg="6"
            cols="12"
          >
            <v-text-field
                v-bind="textFieldStyle"
                :label="$t('administration.users.first_name')"
                v-model="firstname"
                @update:model-value="edited = true"
                @click:clear="firstname = ''"
            />
          </v-col>
          <v-col
              lg="6"
              cols="12"
          >
            <v-text-field
                v-bind="textFieldStyle"
                :label="$t('administration.users.last_name')"
                v-model="lastname"
                @update:model-value="edited = true"
                @click:clear="lastname = ''"
            />
          </v-col>
        </v-row>
        <v-text-field
            ref="emailField"
            v-bind="textFieldStyle"
            :label="$t('administration.users.email')"
            v-model="email"
            :rules="[rules.required, rules.email_free]"
            @update:model-value="checkEmail()"
        />

        <app-password-textfield
            v-if="!edit"
            v-bind="textFieldStyle"
            :label="$t('administration.users.password')"
            v-model="password"
            :rules="[rules.required]"
            @update:model-value="setPasswordEdited()"
            class="mb-4"
        />

        <v-divider
            class="border-opacity-25 mb-4"
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
    <v-card-actions
      class="d-flex justify-end"
    >
      <v-btn
          prepend-icon="mdi-content-save"
          variant="elevated"
          color="primary"
          @click="saveUser()"
          :disabled="!edited || correct != userCorrect"
          :loading="loading"
      >
        {{ $t('administration.users.save_user') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss">
.test{
  //height: 0px;
  overflow-y: scroll
}
</style>