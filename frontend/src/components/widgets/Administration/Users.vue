<script lang="ts">
import {defineComponent} from "vue";
import useAxios from "@/composables/useAxios.ts";
import {AdministrationEndpoint} from "@/api/http/AdministrationEndpoint.ts";
import {User} from "@/types/api.ts";
import {useDisplay} from "vuetify";
import UserEditModal from "@/components/widgets/Administration/Users/UserEditModal.vue";
import {GeneralEndpoint, UserEndpoint} from "@/api/http";

export default defineComponent({
  name: "Users",
  components: {UserEditModal},
  setup(){
    const adminEndpoint = useAxios("administration")
    const userEndpoint = useAxios("user")
    const generalEndpoint = useAxios("general")
    const {mobile} = useDisplay()
    return {
      mobile,
      adminEndpoint: adminEndpoint.axios as AdministrationEndpoint,
      userEndpoint: userEndpoint.axios as UserEndpoint,
      generalEndpoint: generalEndpoint.axios as GeneralEndpoint
    }
  },
  computed:{
    deleteModalActive(){
      return this.usersToDelete.length > 0 && !this.deleting
    },
    headers() {
      let headers: Array<object> = [
        {
          title: this.$t("administration.users.table.headers.username"),
          value: "username"
        },
        {
          title: this.$t("administration.users.table.headers.email"),
          value: "email"
        }
      ]

      if(!this.mobile) {
        headers = headers.concat([
          {
            title: this.$t("administration.users.table.headers.first_name"),
            value: "firstName"
          },
          {
            title: this.$t("administration.users.table.headers.last_name"),
            value: "lastName"
          },
          {
            title: this.$t("administration.users.table.headers.admin"),
            value: "isAdmin",
          },
          {
            title: this.$t("administration.users.table.headers.registered"),
            value: "registrationDate"
          }
        ])
      }

      headers.push({
        title: this.$t("administration.users.table.headers.account_confirmed"),
        value: "emailConfirmed"
      })
    headers.push({
        title: this.$t("administration.users.table.headers.actions"),
        value: "actions"
      })
      return headers
    },
    usersSelected(){
      return this.selected.length > 1 || this.selected.length == this.users.length
    },
    userTOEdit: {
      get(){
        if(this.user === -1){
          return undefined
        }
        return this.users[this.user]
      },
      set(value: (undefined|Partial<User>)){
        if(value === undefined){
          this.user = -1
          return
        }
        this.users[this.user] = value
      }
    },
    deleteConfirmationTitle(){
      if(this.usersToDelete.length === 1){
        return this.$t('administration.users.delete_confirm_title_single')
      }
      return this.$t('administration.users.delete_confirm_title_multiple')
    },
    deleteConfirmationBody(){
      if(this.usersToDelete.length === 1){
        return this.$t('administration.users.delete_confirm_body_single', {name: this.usersToDelete[0].username ?? ''})
      }
      return this.$t('administration.users.delete_confirm_body_multiple', {count: this.usersToDelete.length})

    }
  },
  data() {
    return {
      loading: false,
      users: [] as Array<Partial<User>>,
      search: '',
      searchShown: false,
      selected: [] as Array<Partial<User>>,
      userToEdit: undefined as (undefined|Partial<User>),
      user: -1,
      createModalActive: false,
      usersToDelete: [] as Array<Partial<User>>,
      deleting: false,
      smtpEnabled: false,
      passwordResetModalActive: false,
      userIdForPwReset: undefined as (number|undefined),
      userNameForPwReset: undefined as (string|undefined),
      resettingPassword: false,
      sendingConfirmationEmail: false
    }
  },
  methods:{
    resendEmail(userId: number){
      this.sendingConfirmationEmail = true
      this.adminEndpoint.resendConfirmationEmail(userId).then((success: boolean) => {
        this.sendingConfirmationEmail = false
        if(success){
          this.$notify({
            title: this.$t('toasts.titles.success.resent_confirmation'),
            text: this.$t('toasts.text.success.resent_confirmation'),
            type: "success"
          })
        }
      })

    },
    resetPassword(userId: number, userName: string){
      this.userIdForPwReset = userId
      this.userNameForPwReset = userName
      this.passwordResetModalActive = true

    },
    editUser(user: Partial<User>, index: number){
      this.user = index
    },
    requestDeletion(user: Partial<User>){
      this.usersToDelete.push(user)
    },
    async deleteUser(){
      this.deleting = true;
      let multiple = this.users.length > 1
      let allSuccessful = true;
      let someSuccessful = false;
      let userIds = []
      for(const user of this.usersToDelete){
        const success = await this.userEndpoint.deleteUser(user.id!)
        allSuccessful = allSuccessful && success;
        someSuccessful = someSuccessful || success;
        if(success){
          userIds.push(user.id!)
        }
      }
      this.users = this.users.filter(u => !userIds.includes(u.id!))
      this.deleting = false;
      if(allSuccessful){
        this.$notify({
          title: this.$t(`toasts.titles.success.deleted${multiple ? '_multiple' : ''}`, {count: userIds.length}),
          text: this.$t(`toasts.text.success.deleted${multiple ? '_multiple' : ''}`),
          type: 'success'
        })
      }
      else if(someSuccessful){
        this.$notify({
          title: this.$t(`toasts.titles.info.some_deleted`),
          text: this.$t(`toasts.text.info.some_deleted`),
          type: 'info'
        })
      }
      this.usersToDelete = []
      this.selected = []
    },
    abortDeletion(){
      this.usersToDelete = []
    },
    deleteSelectedUser(){
      this.usersToDelete = [...this.selected];
    },
    createUser(){
      this.createModalActive = true
    },
    userCreated(newUser: User){
      this.users.push(newUser)
    },
  },
  beforeMount(){
    this.loading = true
    this.generalEndpoint.checkSmtp().then((enabled: boolean) => {
      this.smtpEnabled = enabled;
      this.adminEndpoint.loadUsers().then((users) => {
        this.users = users
        this.loading = false
      })
    })

  }
})
</script>

<template>
  <v-row
    justify="center"
  >
    <v-col
      lg="10"
      cols="12"
    >
      <v-dialog
        v-model="deleting"
        :persistent="true"
      >
        <app-progress-circular
            :width="10"
            :size="128"
            :message="$t('administration.users.deleting')"
        />
      </v-dialog>

      <v-dialog
        v-model="resettingPassword"
        :persistent="true"
      >
        <app-progress-circular
            :width="10"
            :size="128"
            :message="$t('administration.users.resetting_password')"
        />
      </v-dialog>

      <user-edit-modal
        v-model="userTOEdit"
      />
      <user-create-modal
        v-model="createModalActive"
        @created:user="userCreated"
      />
      <app-confirm-modal
        :title="deleteConfirmationTitle"
        :body="deleteConfirmationBody"
        :dialog="deleteModalActive"
        @accept="deleteUser"
        @deny="abortDeletion"
      />
      <password-reset-modal
        v-model:active="passwordResetModalActive"
        v-model:user-id="userIdForPwReset"
        :from-admin="true"
        :user-name="userNameForPwReset"
        @update:active="() => {
          userIdForPwReset = undefined
          userNameForPwReset = undefined
        }"
      />

      <v-container :fluid="true" class="pl-0 pr-0">
          <div
            class="mb-4 d-flex justify-end"
          >
            <v-btn
              color="primary"
              density="compact"
              @click="createUser"
            >
              {{ $t('administration.users.create')}}
            </v-btn>
          </div>
          <v-data-table
            v-model="selected"
            ref="userTable"
            :loading="loading"
            :headers="headers"
            :items="users"
            :search="search"
            :show-select="true"
            :return-object="true"
        >
          <template v-slot:header.data-table-select="{ allSelected, selectAll, someSelected }">
            <v-checkbox-btn
                :indeterminate="someSelected && !allSelected"
                :model-value="allSelected"
                color="primary"
                @update:model-value="selectAll(!allSelected)"
            ></v-checkbox-btn>
          </template>

          <template v-slot:item.data-table-select="{ internalItem, isSelected, toggleSelect }">
            <v-checkbox-btn
                :model-value="isSelected(internalItem)"
                color="primary"
                @update:model-value="toggleSelect(internalItem)"
            ></v-checkbox-btn>
          </template>
          <template v-slot:top>
            <v-toolbar
                :flat="true"
                density="compact"
            >

              <template v-slot:title>
                <template
                    v-if="usersSelected"
                >
                  {{ $t('administration.users.selected', {count: selected.length})}}
                </template>
                <template
                    v-else
                >
                  {{ $t('administration.users.table.title') }}
                </template>
              </template>
              <template
                  v-if="!usersSelected"
              >
                <v-btn
                    icon="mdi-magnify"
                    @click="searchShown = true"
                    v-if="!searchShown"
                />
                <v-text-field
                    v-model="search"
                    :label="$t('administration.users.search')"
                    density="compact"
                    color="grey darken-4"
                    :hide-details="true"
                    :single-line="true"
                    v-else
                >
                  <template v-slot:prepend-inner>
                    <v-btn
                        icon="mdi-magnify"
                        @click="searchShown = false"
                    />
                  </template>
                </v-text-field>
              </template>
              <template
                  v-else
              >
                <v-btn
                    icon="mdi-delete"
                    color="red"
                    @click="deleteSelectedUser()"
                />
              </template>
            </v-toolbar>
          </template>
          <template v-slot:item.actions="{item, index}">
            <app-icon-btn
                class="me-2"
                icon="mdi-lock-reset"
                color="primary"
                size="large"
                @click="resetPassword(item.id!, item.username!)"
            />
            <app-icon-btn
                class="me-2"
                icon="mdi-pencil"
                color="yellow-darken-1"
                size="large"
                @click="editUser(item, index)"
            />
            <app-icon-btn
                icon="mdi-delete"
                color="red"
                size="large"
                @click="requestDeletion(item)"
            />
          </template>

          <template v-slot:item.isAdmin="{item}">
            <v-icon
                icon="mdi-check-circle-outline"
                :color="item.isAdmin ? 'green' : 'grey'"
            />
          </template>
          <template
              v-slot:item.emailConfirmed="{item}"
          >
            <v-icon
                v-if="item.emailConfirmed"
                icon="mdi-check-circle-outline"
                color="green"
            />
            <app-icon-btn
                v-else
                icon="mdi-email-sync"
                color="primary"
                size="large"
                :disabled="sendingConfirmationEmail"
                :loading="sendingConfirmationEmail"
                @click="resendEmail(item.id!)"
            />
          </template>

        </v-data-table>
      </v-container>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
:deep(.v-overlay__content) {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>