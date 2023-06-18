

<template>
    <v-toolbar id="navbar" class="cnavbar" :title="this.title" />
    <Slide class="cnavbar" :crossIcon="false" :closeOnNavigation="true">
      <a id="home" @click="this.$router.push('/Home')">
          <span>{{ this.$t("home") }}</span>
      </a>
      <a @click="redirectOrReload('/BoxesOverview', 'boxes')">
        <span>
          {{ this.$t("boxes") }}
        </span>
      </a>
      <a @click="this.$router.push('/LocationsOverview')">
        <span>
          {{ this.$t("locations") }}
        </span>
      </a>
      <a @click="redirectOrReload('/ProductsOverview', 'products')">
        <span>
          {{ this.$t("products") }}
        </span>
      </a>
      <div id="actionIcons" class="d-flex justify-space-evenly">
          <v-list-item density="compact" >
              <v-list-item-subtitle>
                  <v-icon @click="this.logoutUser()" icon="fa:fas fa-sign-out-alt"/>
              </v-list-item-subtitle>
          </v-list-item>
          <v-list-item density="compact" >
              <v-list-item-subtitle>
                  <v-icon icon="fa:fas fa-cog" @click="this.$router.push('/Settings')" />
              </v-list-item-subtitle>
          </v-list-item>
      </div>
    </Slide>

</template>
<script>
import { Slide } from 'vue3-burger-menu';
import {logout} from "@/db/dexie";
import {resetLangToDefault} from "@/global/constants";

export default {
    name: 'App',
    components: {
        Slide
    },
    data() {
        return {
        }
    },
    props: {
      title: {
        type: String,
        default: "InventoryHero"
      }
    },
    methods: {
      logoutUser(){
        logout().then(() => {
            this.$i18n.locale = resetLangToDefault();
            this.$router.push("/");
        });
      },

      redirectOrReload(path, view)
      {
        if(view !== this.$route.name) {
          this.$router.push({path: path});
        }
        else{
          this.$emit("reload"+view);
        }
      }
    }
}
</script>
a:visited {
color: white;
}
<style scoped>
#navbar {
    top: 0;
    background-color: var(--color-dark-theme-lighter);
    color: white;
    height: 60px !important
}
#actionIcons {
    position: absolute;
    bottom: 0vh;
    width: 85%;
}
.cnavbar{
    position: fixed;
    z-index: 1000;
}
</style>