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
        <transition :name="animationName" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.slide-left-enter-active{
  transition: all 0.5s ease-in-out;
}

.slide-left-leave-active{
  transition: all 0.75s ease-in-out;
}

.slide-left-enter-from {
  transform: scale(0.75);
}

.slide-left-leave-to {
  transform: translateX(-110%);
}

.slide-right-enter-active{
  transition: all 0.5s ease-in-out;
}
.slide-right-leave-active {
  transition: all 0.75s ease-in-out;
}

.slide-right-leave-to{
  transform: translateX(110%);
}

.slide-right-enter-from {
  transform: scale(0.75);
}





</style>