<template>
    <div id="containerSearchBar" :class="this.theme">
        <input :class="this.do_transform" type="text" v-model="this.value" @input="this.$emit('valueUpdated', this.value)">
        <i class="fa-solid fa-magnifying-glass fa-lg icon"></i>
    </div>
</template>

<script>
import {getSettings} from "@/db/dexie"


export default {
    name: 'searchBar',
    data() {
          return {
              value: "",
              theme: ""
          }
      },
    props: {
        do_transform: {
            type: String,
            default: "transform",
        }
    },
     beforeMount() {
         getSettings().then((settings) => {
             this.theme =  settings.theme;
         })
     }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#containerSearchBar{ 
    position: relative;
    width: 80%;
    height: 50px;
    margin-left: 50%;
    margin-bottom: 10px;
    transform: translateX(-50%);
    top: 15px;
    border-radius: 25px;
}

.light-theme  {
    background-color: var(--color-light-theme-lighter);
    border: rgba(0, 0, 0, 0.6) solid 2px;
}
.dark-theme  {
    background-color: var(--color-dark-theme-lighter);
    border: rgba(255, 255, 255, 0.6) solid 2px;
}

.light-theme input  {
    background-color: rgba(255,255,255,0.6);
    color: black;
}
.dark-theme input  {
    background-color: rgba(0,0,0,0.6);
    color: white;
}

.dark-theme i  {
    color: white;
}
.light-theme i  {
    color: rgba(0, 0, 0, 0.6);
}

.transform{
    transform: translateX(-50%);
}
.icon {
    position: absolute;
    left: 20px;
    top: 21px;
    transform: translateY(-50%);
}

input {
    position: absolute;
    width: 100%;
    height: 100%;
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding-left: 50px;
    color: white;
}

input:focus{
    outline: none;
    border-color: inherit;
    -webkit-box-shadow: none;
    box-shadow: none;
}

</style>
  