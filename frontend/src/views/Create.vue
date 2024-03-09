<script lang="ts">
import {defineComponent} from 'vue'
import {RouteLocationNormalized, useRoute} from "vue-router";

export default defineComponent({
  name: "Create",
  setup(){
    const route = useRoute();
    return {route}
  },
  data(){
    return {
      confirm: false,
      forceLeave: false,
      to: '/',
      animationName: "slide-left"
    }
  },
  beforeRouteUpdate(to, from){
    let direction = this.addRoutes.indexOf(to.fullPath) - this.addRoutes.indexOf(from.fullPath)
    if (direction == -1 || direction == (this.addRoutes.length - 1)){
      this.animationName = "slide-right"
    }
    else{
      this.animationName = "slide-left"
    }

  },
  computed: {
    addRoutes(){
      // child routes of create in order to allow swipe navigation
      return ["/create/product", "/create/box", "/create/location"]
    },
    currentRoute(){
      return this.addRoutes.indexOf(this.route.fullPath)
    }
  },
  methods:{
    leave(){
      this.confirm = false
      this.forceLeave = true
      this.$router.push(this.to)
    },
    stay(){
      this.confirm = false
      this.to = "/"
    },
    swipe (direction: "Right"|"Left"|"Up"|"Down") {
      let dir = 0
      switch(direction){
        case "Right":
          dir = -1
          break
        case "Left":
          dir = +1
          break
      }

      let newRoute = (((this.currentRoute+dir) % (this.addRoutes.length)) + this.addRoutes.length) % this.addRoutes.length

      this.$router.push(this.addRoutes[newRoute])
    }

  },
  beforeRouteLeave (to, from) {
    if(this.forceLeave)
    {
      this.forceLeave = false
      return true
    }
    this.to = to.fullPath
    this.confirm = true
    return false
  }
})
</script>

<template>

  <v-row
      :no-gutters="true"
      class="justify-center fill-height"
      v-touch="{
        left: () => swipe('Left'),
        right: () => swipe('Right'),
        up: () => swipe('Up'),
        down: () => swipe('Down')
      }"

  >
    <v-col
        cols="12"
        lg="6"
    >
      <app-confirm-modal
        :dialog="confirm"
        :title="$t('confirm.leave.title')"
        :body="$t('confirm.leave.text')"
      >
        <v-btn
            prepend-icon="fa:fas fa-ban"
            @click="stay()"
        >
          {{ $t('confirm.leave.deny') }}
        </v-btn>
        <v-btn
            prepend-icon="fa:fas fa-check-circle"
            @click="leave()"
        >
          {{ $t('confirm.leave.accept') }}
        </v-btn>
      </app-confirm-modal>
      <router-view v-slot="{Component}">
        <transition :name="animationName">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.slide-left-enter-active,
 .slide-left-leave-active {
   transition: all 0.75s ease-out;
 }

.slide-left-enter-to {
  position: fixed;
  right: 0;
  top: calc(var(--v-layout-top) + 16px);
}

.slide-left-enter-from {
  position: fixed;
  right: -100%;
  top: calc(var(--v-layout-top) + 16px);
}

.slide-left-leave-to {
  position: fixed;
  left: -100%;
  top: calc(var(--v-layout-top) + 16px);
}

.slide-left-leave-from {
  position: fixed;
  left: 0;
  top: calc(var(--v-layout-top) + 16px);
}



.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.75s ease-out;
}

.slide-right-leave-to{
  position: fixed;
  right: -100%;

  top: calc(var(--v-layout-top) + 16px);
}

.slide-right-leave-from{
  position: fixed;
  right: 0;
  top: calc(var(--v-layout-top) + 16px);
}


.slide-right-enter-to {
  position: fixed;
  left: 0;
  top: calc(var(--v-layout-top) + 16px);
}


.slide-right-enter-from{
  position: fixed;
  left: -100%;
  top: calc(var(--v-layout-top) + 16px);
}


</style>