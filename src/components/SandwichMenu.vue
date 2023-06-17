

<template>
    <v-toolbar id="navbar" class="cnavbar" :title="this.title" />
    <Slide class="cnavbar" :crossIcon="false">
      <a id="home" @click="this.$router.push('/Home')">
          <span>Home</span>
      </a>
      <a @click="redirectOrReload('/BoxesOverview')">
        <span>
      Boxes
        </span>
      </a>
      <a @click="redirectOrReload('/LocationsOverview')">
        <span>
          Locations
        </span>
      </a>
      <a @click="redirectOrReload('/ProductsOverview')">
        <span>
          Products
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
              this.$router.push("/");
          });
        },
      redirectOrReload(path)
      {
        this.$router.push({path: path}).then(()=> {this.$router.go()})
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
    background-color: var(--color-darker);
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