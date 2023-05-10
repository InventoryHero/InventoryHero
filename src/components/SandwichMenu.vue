

<template>
    <v-toolbar id="navbar" absolute fixed :title='this.title'>
    </v-toolbar>
    <Slide @openMenu="this.showTitle=false" @closeMenu="this.showTitle=true" :crossIcon="false" :closeOnNavigation="true" enableOutsideClick>
        <a id="home" href="#">
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
        <a href="">
      <span>
        Products
      </span>
        </a>
    </Slide>


</template>
<script>
import { Slide } from 'vue3-burger-menu';

export default {
    name: 'App',
    components: {
        Slide
    },
    data() {
        return {
            showTitle: true,
        }
    },
    props: ["title"],
    methods: {
        openMenu() {
            console.log("open me")
        },
    }
}
</script>
a:visited {
color: white;
}
<style>
#navbar {
    position: absolute;
    top: 0vh;
    background-color: var(--color-darker);
    color: white;

}
.bm-burger-bars {
    background-color: white !important;
}
.bm-burger-button {
    position: absolute;
    top: 2vh !important;
    left: 4% !important;
}
</style>