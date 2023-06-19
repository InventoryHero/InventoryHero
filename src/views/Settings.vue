<template>

  <h1 id="posLanguage">{{ this.$t('settings_view.language') }}</h1>
  <div class="containerFlags">
    <span class="fi fi-um flag" :class="{selected: selected==='en'}" @click="changeLocale('en')" ></span>
    <span class="fi fi-de flag" :class="{selected: selected==='de'}" @click="changeLocale('de')" ></span>
    <span class="fi fi-it flag" :class="{selected: selected==='it'}" @click="changeLocale('it')" ></span>
  </div>

  <h1 id="posTheme">{{ this.$t('settings_view.theme') }}</h1>
  <div class="containerTheme">
    <div class="circle dark" :class="{selected: selected_theme==='dark-theme'}" @click="changeTheme('dark-theme')" ></div>
    <div class="circle light" :class="{selected: selected_theme==='light-theme'}"
                  @click="changeTheme('light-theme')" ></div>
  </div>

  <SandwichMenu :title="this.$t('settings_view.settings')"/>

</template>

<script>
import SandwichMenu from "@/components/SandwichMenu.vue";
import {getSettings, setLanguage, setTheme} from "@/db/dexie"

export default {
name: 'App',
components: {
  SandwichMenu
},
data() {
  return {
    selected: this.$i18n.locale,
    selected_theme: "",
    theme: ""
  }
},
methods: {
  changeLocale(lang)
  {
    this.selected = lang;
    this.$i18n.locale = lang;
    setLanguage(lang);
  },
  changeTheme(to) {
    setTheme(to).then(() => {});
  }
}, beforeMount() {
    getSettings().then((settings) => {
      this.theme =  settings.theme;
    })
}
}
</script>

<style scoped>
.flag {
  font-size: 3em;
  cursor: pointer;
}

span {
  margin-right: 10vw;
  transform: translateX(50%);
}

.containerFlags {
  position: relative;
  top: 12vh;
}

.selected {
  box-shadow: 0px 0px 10px 5px #888888;;
}

#posTheme {
  margin-top: 20vh;
}

.circle {
  width: 3em;
  height: 3em;
  border-radius: 10vw;
  margin-right: 20px;
  transform: translateX(10px);
  cursor: pointer;
}

.containerTheme {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 2.5vh;
}

.light {
  border: 1px solid black;
  background-color: rgb(255, 242, 202);
}

.dark {
  border: 1px solid white;
  background-color: rgb(35, 35, 35);
}

#posLanguage {
  position: relative;
  top: 10vh;
}
</style>
