<script lang="ts">
import {defineComponent} from 'vue'
import {RouteLocationNormalized} from "vue-router";

export default defineComponent({
  name: "Create",
  data(){
    return {
      confirm: false,
      forceLeave: false,
      to: '/'
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
        <transition name="slide">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.slide-enter-active,
.slide-leave-active {
  transition: all 0.75s ease-out;
}

.slide-enter-to {
  position: fixed;
  right: 0;
  top: calc(var(--v-layout-top) + 16px);
}

.slide-enter-from {
  position: fixed;
  right: -100%;
  top: calc(var(--v-layout-top) + 16px);
}

.slide-leave-to {
  position: fixed;
  left: -100%;
  top: calc(var(--v-layout-top) + 16px);
}

.slide-leave-from {
  position: fixed;
  left: 0;
  top: calc(var(--v-layout-top) + 16px);
}
</style>