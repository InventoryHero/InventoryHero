import { defineStore } from 'pinia'
import { useGeneralSocketStore, useHouseholdSocketStore } from '@/stores'
import { HouseholdPublic } from '@/api/types/households.ts'
import { UserPublic } from '@/api/types/user.ts'

export default defineStore('auth', {
  state: () => ({
    user: undefined as UserPublic | undefined,
    household: undefined as HouseholdPublic | undefined,
    authorized: false,
    permissions: {}
  }),
  actions: {
    async whoami() {
      const { userEndpoint } = useAxios()
      const { success, data: user } = await userEndpoint.self()
      if (!success) {
        // TODO HANDLE
        return
      }

      this.user = user
    },
    async reset() {
      this.user = undefined
      this.household = undefined
      this.authorized = false
      /*const generalSocket = useGeneralSocketStore()
            const householdSocket = useHouseholdSocketStore()
            generalSocket.updateHeaders()
            householdSocket.updateHeaders()*/
    },
    async logout() {
      const { auth } = useAxios()
      await auth.logout()
      await this.reset()
    },

    async destroy() {
      const socketStore = useHouseholdSocketStore()
      //socketStore.leaveHousehold()
      const generalSocketStore = useGeneralSocketStore()
      //generalSocketStore.leave()
      await this.reset()
    },
    async getDefaultHousehold() {
      const { userEndpoint } = useAxios()
      const { success, data: defaultHousehold } =
        await userEndpoint.getDefaultHousehold()
      if (!success) {
        // TODO HANDLE
        this.authorized = false
        return
      }
      this.household = defaultHousehold
      this.authorized = true
    }
  },
  getters: {
    isAdmin: (state) => {
      return false
    }
  }
})
