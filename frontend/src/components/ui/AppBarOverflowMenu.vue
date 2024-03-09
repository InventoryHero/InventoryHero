<script lang="ts">
import {useAuthStore} from "@/store/index.ts";
import {defineComponent} from "vue";

export default defineComponent({
  name: "AppBarOverflowMenu",
  setup(){
    const auth = useAuthStore();
    return {auth}
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
            icon="fa:fas fa-user-circle"
            variant="flat"

        >
        </v-btn>


      </template>
      <v-list
          class="mt-2"
          density="compact"
          :nav="true"
      >
        <nav-item
          route="/account"
          icon="fa:fas fa-user"
          :title="$t('nav.account')"
          size="small"
        />
        <v-divider/>
        <nav-item
            route="/households"
            icon="fa:fas fa-house-user"
            :title="$t('nav.households')"
            size="small"
        />
        <v-divider/>
        <nav-item
            route="/settings"
            icon="fa:fas fa-gears"
            :title="$t('nav.settings')"
            size="small"
        />
        <v-divider color="primary" class="border-opacity-50"/>


        <v-list-item
            @click="logout()"
        >
          <template #prepend>
            <v-icon
                icon="fa:fas fa-arrow-right-from-bracket"
                size="small"
              />
          </template>
          <v-list-item-title>
            {{ $t('nav.logout') }}
          </v-list-item-title>
        </v-list-item>
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