<script lang="ts">
import {defineComponent} from "vue";
import useAxios from "@/composables/useAxios.ts";
import {AdministrationEndpoint} from "@/api/http/AdministrationEndpoint.ts";
import {User} from "@/types/api.ts";
import {useDisplay} from "vuetify";
import UserEditModal from "@/components/widgets/Administration/Users/UserEditModal.vue";
import {UserEndpoint} from "@/api/http";


//TODO RESEND EMAIL VERIFICATION

export default defineComponent({
  name: "Users",
  components: {UserEditModal},
  setup(){
    const adminEndpoint = useAxios("administration")
    const userEndpoint = useAxios("user")
    const {mobile} = useDisplay()
    return {
      mobile,
      adminEndpoint: adminEndpoint.axios as AdministrationEndpoint,
      userEndpoint: userEndpoint.axios as UserEndpoint

    }
  },
  computed:{
    deleteModalActive(){
      return this.usersToDelete.length > 0 && !this.deleting
    },
    headers() {
      let headers: Array<Object> = [
        {
          title: "Username",
          value: "username"
        },
        {
          title: "E-Mail",
          value: "email"
        }
      ]

      if(!this.mobile) {
        headers = headers.concat([
          {
            title: "First Name",
            value: "first_name"
          },
          {
            title: "Last Name",
            value: "last_name"
          },
          {
            title: "Admin",
            value: "is_admin",
          },
          {
            title: "Registered",
            value: "registration_date"
          }
        ])
      }
      headers.push({
        title: "Email confirmed",
        value: "email_confirmed"
      })
    headers.push({
        title: "Actions",
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
        return this.$t('administration.users.delete_confirm_title')
      }
      return "delete selected users?"
    },
    deleteConfirmationBody(){
      if(this.usersToDelete.length === 1){
        return this.$t('administration.users.delete_confirm_body')
      }
      return "really?"
    }
  },
  data() {
    return {
      loading: false,
      users: [] as Array<Partial<User>>,
      search: '',
      searchShown: false,
      selected: [] as Array<number>,
      userToEdit: undefined as (undefined|Partial<User>),
      user: -1,
      createModalActive: false,
      usersToDelete: [] as Array<number>,
      deleting: false
    }
  },
  methods:{
    resendEmail(userId: number){
      this.adminEndpoint.resendConfirmationEmail(userId).then((success: boolean) => {
        if(success){
          this.$notify({
            title: this.$t('toasts.titles.success.resent_confirmation'),
            text: this.$t('toasts.text.success.resent_confirmation'),
            type: "success"
          })
        }
      })

    },
    editUser(user: Partial<User>, index: number){
      this.user = index
    },
    requestDeletion(id: number){
      this.usersToDelete.push(id)
    },
    async deleteUser(){
      this.deleting = true;
      let multiple = this.users.length > 1
      let allSuccessful = true;
      for(const user of this.usersToDelete){
        const success = await this.userEndpoint.deleteUser(user)
        allSuccessful = allSuccessful && success;
        if(success){
          this.users = this.users.filter((u) => {
            return u.id !== user
          })
        }
      }
      this.deleting = false;

      let type = allSuccessful ? "success" : "error";
      this.$notify({
        title: this.$t(`toasts.titles.${type}.deleted${multiple ? '_multiple' : ''}`),
        text: this.$t(`toasts.text.${type}.deleted${multiple ? '_multiple' : ''}`),
        type: 'success'
      })
      this.usersToDelete = []
      this.selected = []
    },
    abortDeletion(){
      this.usersToDelete = []
    },
    deleteSelectedUser(){
      this.usersToDelete = this.selected;
    },
    createUser(){
      this.createModalActive = true
    },
    userCreated(newUser: User){
      this.users.push(newUser)
    }
  },
  mounted(){
    this.loading = true
    this.adminEndpoint.loadUsers().then((users) => {
      this.users = users
      this.loading = false
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
            :headers="headers"
            :items="users"
            item-value="id"
            :search="search"
            :show-select="true"
        >
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
                  {{ $t('administration.users.table') }}
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
                icon="mdi-pencil"
                color="primary"
                size="large"
                @click="editUser(item, index)"
            />
            <app-icon-btn
                icon="mdi-delete"
                color="red"
                size="large"
                @click="requestDeletion(item.id)"
            />
          </template>

          <template v-slot:item.is_admin="{item}">
            <v-icon
                icon="mdi-check-circle-outline"
                :color="item.is_admin ? 'green' : 'grey'"
            />
          </template>
          <template v-slot:item.email_confirmed="{item}">
            <v-icon
                v-if="item.email_confirmed"
                icon="mdi-check-circle-outline"
                color="green"
            />
            <app-icon-btn
                v-else
                icon="mdi-email-sync"
                color="primary"
                size="large"
                @click="resendEmail(item.id)"
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