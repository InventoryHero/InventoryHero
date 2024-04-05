<script lang="ts">
import {defineComponent, PropType} from "vue";
import {User} from "@/types/api.ts";
import {useDisplay} from "vuetify";
import {useSocketStore} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";

export default defineComponent({
  name: "UserCard",
  setup(){
    const {mobile} = useDisplay()
    const sockets = useSocketStore()
    const {axios} = useAxios("user")
    return {
      mobile,
      sockets,
      userEndpoint: axios as UserEndpoint
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
        class: "mb-4"
      }
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
    }
  },
  data(){
    return {
      edited: false,
      updatedUserData: {} as Partial<User>,
      rules: {
        required: (value: string) => !!value || this.$t('administration.users.edit.rules.field_required')
      }
    }
  },
  methods:{
    reset(){
      this.updatedUserData = {}
      this.$refs.form.reset()
      this.edited = false
    },
    async saveUser(){
      if(!this.edited){
        return
      }
      const {valid} = await this.$refs.form.validate()
      if(!valid){
        return
      }
      this.$emit('click:save', this.updatedUserData)
    }
  },
  unmounted() {
    this.updatedUserData = {}
    this.edited = false
  }
})
</script>

<template>
  <v-card
    v-bind="$attrs"
    min-height="60vh"
    :max-height="mobile ? '100vh' : '90vh' "
    class="d-flex flex-column"
  >
    <v-card-title
      class="d-flex align-center shadowed flex-0-0"
    >
      {{ $t('administration.users.edit.title') }}
      <v-spacer />
      <v-fade-transition>
        <v-btn
            v-if="edited"
            class="me-4"
            density="comfortable"
            prepend-icon="mdi-lock-reset"
            variant="tonal"
            @click="reset()"
        >
          {{ $t('administration.users.edit.reset') }}
        </v-btn>
      </v-fade-transition>
      <app-icon-btn
        icon="mdi-close"
        @click="$emit('close')"
      />
    </v-card-title>
    <v-card-text
      class="mt-4 test flex-1-1 overflow-auto"
    >
      <v-form
        ref="form"

      >
        <v-text-field
            v-bind="textFieldStyle"
            :label="$t('administration.users.edit.username')"
            v-model="username"
            :rules="[rules.required]"
            @update:model-value="edited = true"
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
                :label="$t('administration.users.edit.firstname')"
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
                :label="$t('administration.users.edit.lastname')"
                v-model="lastname"
                @update:model-value="edited = true"
                @click:clear="lastname = ''"
            />
          </v-col>
        </v-row>
        <v-text-field
            v-bind="textFieldStyle"
            :label="$t('administration.users.edit.email')"
            v-model="email"
            :rules="[rules.required]"
            @update:model-value="edited = true"
        />

        <app-password-textfield
            v-if="!edit"
            v-bind="textFieldStyle"
            :label="$t('administration.users.edit.password')"
            v-model="password"
            :rules="[rules.required]"
            @update:model-value="edited = true"
            class="mb-4"
        />


        <v-divider
            class="border-opacity-25 mb-4"
            color="primary"
            :thickness="2"
        />
        <p class="text-h5">
          {{ $t('administration.users.edit.roles')}}
        </p>
        <v-checkbox
          :label="$t('administration.users.edit.admin')"
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
          :disabled="!edited"
          :loading="loading"
      >
        {{ $t('administration.users.edit.save_user') }}
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