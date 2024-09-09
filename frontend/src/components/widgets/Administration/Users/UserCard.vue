<script lang="ts">
import {defineComponent, PropType} from "vue";
import {User} from "@/types/api.ts";
import {useDisplay} from "vuetify";
import {useGeneralSocketStore, useHouseholdSocketStore} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import AppResetButton from "@/components/ui/AppResetButton.vue";

export default defineComponent({
  name: "UserCard",
  components: {AppResetButton},
  setup(){
    const {mobile} = useDisplay()
    const sockets = useHouseholdSocketStore()
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
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
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
        if(this.updatedUserData.firstName !== undefined){
          return this.updatedUserData.firstName
        }
        return this.user?.firstName ?? ''
      },
      set(firstname: string){
        this.updatedUserData.firstName = firstname
      }
    },
    lastname:{
      get(){
        if(this.updatedUserData.lastName !== undefined){
          return this.updatedUserData.lastName
        }
        return this.user?.lastName ?? ''
      },
      set(lastname: string){
        this.updatedUserData.lastName = lastname
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
        if(this.updatedUserData.isAdmin !== undefined){
          return this.updatedUserData.isAdmin
        }
        return this.user?.isAdmin ?? false
      },
      set(admin: boolean){
        this.updatedUserData.isAdmin = admin
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
      } as Partial<object>
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
      valid: false,
      updatedUserData: {} as Partial<User>,
      usernameFree: true,
      emailFree: true,
      rules: {
        required: (value: string) => !!value || this.$t('administration.users.rules.field_required'),
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        username_free: (value: string) => {
          if(this.usernameFree){
            return
          }
          return this.$t('administration.users.rules.username_taken')
        },
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        email_free: (_: string) => {
          if(this.emailFree){
            return
          }
          return this.$t('administration.users.rules.email_taken')
        }
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
      this.generalSocket.isUserNameTaken(this.updatedUserData.username ?? '').then((isTaken) => {
        this.usernameFree = !isTaken
      })
      //this.generalSocket.isUserNameTaken(, callback)
    },
    checkEmail(){
      this.edited = true;
      this.generalSocket.isEmailTaken(this.updatedUserData.email ?? '').then((isTaken) => {
        this.emailFree = !isTaken
      })
    },
    setPasswordEdited(){
      this.edited = true;
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
          :disabled="!edited || !valid"
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