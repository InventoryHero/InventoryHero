

<template>
    <v-toolbar id="navbar" absolute fixed>
    </v-toolbar>
    <Slide :crossIcon="false">
      <a id="home" href="#" @click="this.$router.push('/Home')"> 
          <span>Home</span>
      </a>
      <a href="">
        <span>
      Boxes
        </span>
      </a>
      <a @click="this.$router.push('/LocationsOverview')">
        <span>
          Locations
        </span>
      </a>
      <a @click="this.$router.push('/ProductsOverview')"> 
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
                  <v-icon icon="fa:fas fa-cog"/>
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
    props: ["title"],
    methods: {
        logoutUser(){
          logout().then(() => {
              this.$router.push("/");
          });
        },
    }
}
</script>
a:visited {
color: white;
}
<style scoped>
#navbar {
    position: absolute;
    top: 0vh;
    background-color: var(--color-darker);
    color: white;

}
#actionIcons {
    position: absolute;
    bottom: 0vh;
    width: 85%;
}
</style>