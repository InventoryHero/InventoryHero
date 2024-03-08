<script lang="ts">
import {defineComponent, PropType} from 'vue'
import iro from '@jaames/iro';
import {IroColorPicker, ColorPickerProps} from "@jaames/iro/dist/ColorPicker";
import {IroColor} from "@irojs/iro-core";


type SupportedEvents = 'color:change' | 'color:init'

// PRETTY MUCH TAKEN FROM
// https://github.com/fluidd-core/fluidd/blob/develop/src/components/ui/AppIroColorPicker.vue

export default defineComponent({
  name: "IroColorPicker",
  emits:{
    "color:change"(payload: IroColor){
      return true;
    },
    "color:init"(payload: IroColor){
      return true;
    },
    "input:end"(payload: IroColor){
      return true;
    }

  },
  watch: {
    color(){
        if(this.colorPicker)
        {
          this.colorPicker.color.hexString = this.color
        }
    }

  },
  props: {
    options:{
      type:  Object as PropType<ColorPickerProps>,
      default: {}
    },
    color: {
      type: String,
      default: "#ffffff"
    }
  },
  computed: {
    opts(){
      return {
        ...this.options,
        color: this.color,
        sliderSize: 14
      }
    }
  },
  data(){
    return {
      colorPicker: null as (null | IroColorPicker),
    }
  },
  methods:{
    eventHandler(event: string, color: IroColor){
      this.$emit(event, color)
    }
  },
  mounted(){
    this.colorPicker = iro.ColorPicker(this.$refs.picker as HTMLElement, this.opts)

    if(this.colorPicker)
    {
      this.colorPicker.on("color:init", (color: IroColor) => {
        this.eventHandler("color:init", color)
      })
      this.colorPicker.on("color:change", (color: IroColor) => {
        this.eventHandler('color:change', color)
      })
      this.colorPicker.on("input:end", (color: IroColor) => {
        this.eventHandler('input:end', color)
      })
    }
  },
  beforeUnmount(){
    if(this.colorPicker)
    {
      this.colorPicker.off("color:init", this.eventHandler)
      this.colorPicker.off("color:change", this.eventHandler)
      this.colorPicker.off('input:end', this.eventHandler)
    }
  }
})
</script>

<template>
<div>
  <div ref="picker" />
</div>
</template>

<style scoped lang="scss">

</style>