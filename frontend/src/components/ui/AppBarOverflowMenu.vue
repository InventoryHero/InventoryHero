<script lang="ts">
import {useAuthStore} from "@/store/index.ts";
import {defineComponent} from "vue";

export default defineComponent({
  name: "AppBarOverflowMenu",
  setup(){
    const auth = useAuthStore();
    return {auth}
  },
  computed:{
    isAdmin(){
      return this.auth.isAdmin
    }
  },
  methods:{
    async logout() {
      this.loggingOut=true
      await this.auth.logout();
    },
  },
  data(){
    return{
      loggingOut: false
    }
  }
})
</script>

<template>

    <v-menu
    >
      <template #activator="{props}">
        <v-btn
            v-bind="props"
            icon="mdi-account-circle"
            variant="flat"

        >
        </v-btn>


      </template>
      <v-list
          class="mt-2"
          density="compact"
          nav
      >
        <v-list-item
            to="/account"
            prepend-icon="mdi-account"
            :title="$t('nav.account')"
            color="primary"
        />
        <v-divider/>
        <v-list-item
            to="/households"
            prepend-icon="mdi-home-account"
            :title="$t('nav.households')"
            color="primary"
        />
        <v-divider/>
        <v-list-item
            to="/settings"
            prepend-icon="mdi-cog"
            :title="$t('nav.settings')"
            color="primary"
        />
        <template
            v-if="isAdmin"
        >
          <v-divider/>
          <v-list-item
              to="/administration"
              prepend-icon="mdi-shield-account"
              :title="$t('nav.administration')"
              color="primary"
          />
        </template>
        <v-divider color="primary" class="border-opacity-50"/>
        <v-list-item
            @click="logout()"
            :title="$t('nav.logout')"
            prepend-icon="mdi-logout"

        />
      </v-list>
    </v-menu>
</template>

<style scoped lang="scss">


.dropdown-list{
  background-color: var(--clr-user-dropdown-bg) !important;
  backdrop-filter: blur(2px) !important;
  border: var(--clr-border-alpha) 1px solid;
  border-radius: 10px;
  width: fit-content;
  text-align: start;
}

.active
{
  color: var(--clr-filter-pressed);
}
.inactive{
  color: var(--clr-icon-inactive);
}

.add-pad{
  padding-right: 20px;
}

.icon-text{
  font-weight: bold;
}
</style>