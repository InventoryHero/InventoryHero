<script lang="ts">
  import {defineComponent} from "vue";

  export default defineComponent({
    name: "AppIconBtn",
    emits: {
      click(){
        return true;
      }
    },
    computed: {
      cssClass(){
        let dict = {} as {[key: string] : boolean}
        this.class.split(" ").forEach(x => {dict[x] = true})
        return dict
      }
    },
    methods: {
      clicked()
      {
        if(!this.disabled)
        {
          this.$emit("click")
        }
      },
    },
    props:{
      icon:{
        type: String,
        default: ''
      },
      disabled: {
        type: Boolean,
        default: false
      },
      color:{
        type: String,
        default: "",
      },
      size: {
        default: "1x"
      },
      class: {
        type: String,
        default: ''
      }
    }
  })
</script>

<template>

    <v-hover>
      <template v-slot:default="{isHovering, props}">
        <v-icon
            v-bind="props"
            :icon="icon"
            :size="size"
            :color="color"
            fixed-width
            class="app-font-awesome-btn"
            :class="{
              'hovering': isHovering && !disabled,
              'disabled': disabled,
              ...cssClass
            }"

            @click="clicked()"
        />
      </template>
    </v-hover>

</template>

<style scoped lang="scss">
.disabled{
  &.v-theme--dark{
    color: rgba(255, 255, 255, 0.65) !important;
  }
  &.v-theme--light{
    color: rgba(255, 255, 255, 0.65) !important;
  }
}
.hovering{
  cursor: pointer;
  color: rgba(var(--v-theme-primary), 0.65);

}
</style>