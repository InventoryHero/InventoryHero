<script setup lang="ts">
import {useAuthStore} from "@/store/index.ts";
import {computed} from "vue";
const auth = useAuthStore();
const isAdmin = computed(() =>{
  return auth.isAdmin
})



</script>

<template>

    <v-menu
    >
      <template #activator="{props}">
        <app-icon-btn
            v-bind="props"
            icon="mdi-account-circle"
            size="x-large"
        />


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
            to="/logout"
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