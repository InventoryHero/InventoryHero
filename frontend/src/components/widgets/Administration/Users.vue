<script lang="ts">
import {defineComponent} from "vue";
import useAxios from "@/composables/useAxios.ts";
import {AdministrationEndpoint} from "@/api/http/AdministrationEndpoint.ts";
import {User} from "@/types/api.ts";
import {useDisplay} from "vuetify";
import UserEditModal from "@/components/widgets/Administration/Users/UserEditModal.vue";
import {UserEndpoint} from "@/api/http";

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
      return this.usersToDelete.length > 0
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
      return ""
    },
    deleteConfirmationBody(){
      if(this.usersToDelete.length === 1){
        return this.$t('administration.users.delete_confirm_body')
      }
      return ""
    }
  },
  data() {
    return {
      loading: false,
      users: [] as Array<Partial<User>>,
      search: '',
      searchShown: false,
      selected: [],
      userToEdit: undefined as (undefined|Partial<User>),
      user: -1,
      createModalActive: false,
      usersToDelete: [] as Array<number>
    }
  },
  methods:{
    resendEmail(userId: number){
      console.log("RESEND USER CONFIRMATION EMAIL")
    },
    editUser(user: Partial<User>, index: number){
      //console.log(index)
      this.user = index
      //this.userToEdit = user
    },
    requestDeletion(id: number){
      this.usersToDelete.push(id)
    },
    async deleteUser(){
      // TODO BLOCK USER ROUTES IF USER IS DELETED
      const success = await this.userEndpoint.deleteUser(this.usersToDelete[0])
      if(success){

        this.users = this.users.filter((user) => user.id !== this.usersToDelete[0])

        this.$notify({
          title: this.$t('toasts.titles.success.deleted'),
          text: this.$t('toasts.text.success.deleted'),
          type: 'success'
        })
      }
      this.usersToDelete = []
    },
    abortDeletion(){
      this.usersToDelete = []
    },
    deleteSelectedUser(){
      console.log("delete selected user", this.selected);
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

</style>