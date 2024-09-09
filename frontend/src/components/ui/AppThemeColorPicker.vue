<script lang="ts">
import {defineComponent} from 'vue'
import iro from "@jaames/iro";
import IroColorPicker from "@/components/ui/IroColorPicker.vue";
import {useConfigStore} from "@/store";
import { ColorPickerProps} from "@jaames/iro/dist/ColorPicker";
import {IroColor} from "@irojs/iro-core";


// PRETTY MUCH TAKEN FROM
// https://github.com/fluidd-core/fluidd/blob/develop/src/components/ui/AppColorPicker.vue




export default defineComponent({
  name: "AppThemeColorPicker",
  components: {IroColorPicker},
  setup(){
    const config = useConfigStore();
    return {config}
  },
  props: {
    title: {
      type: String,
      default: ""
    },
    reset:{
      type: String,
      default: ""
    }
  },
  watch: {

    "config.color"(){
      const color = new IroColor(this.config.color)
      this.color.hex = color.hexString
      this.color.rgb = {...color.rgb}
    }
  },
  data(){
    return {
      menu: false,
      color: {
        hex: this.config.color,
        rgb: {
          ...(new iro.Color(this.config.color)).rgb
        }
      },
      options:  {
        width: 208,
        layout: [
          {
            component: iro.ui.Wheel,
            options: {
              wheelLightness: false,
              wheelAngle: 270,
              wheelDirection: 'clockwise'
            }
          },
          {
            component: iro.ui.Slider,
            options: {
              sliderType: 'value'
            }
          }
        ]
      } as ColorPickerProps
    }
  },
  methods:{

    getColor(c: IroColor)
    {
      this.color = {
        hex: c.hexString,
        rgb: {
          r: c.rgb.r,
          g: c.rgb.g,
          b: c.rgb.b
        }
      }
    },
    changeColor(c: IroColor)
    {
      this.getColor(c)
    },
    changeChannel(newValue: number, channel: 'r'|'g'|'b'){
      const currRgb = {
        ...this.color.rgb
      }
      currRgb[channel] = newValue
      const iroColor = new iro.Color(currRgb)
      this.color.hex = iroColor.hexString;
      this.updateColor(iroColor)
    },
    updateColor(c: IroColor)
    {
      this.config.themeChange({
        color: c.hexString
      })
    }
  },
  mounted(){
  }
})
</script>

<template>
<v-menu
    v-model="menu"
    location="left bottom"
    origin="overlap"
    :close-on-content-click="false"
>
  <template v-slot:activator="{ props }">
    <v-btn
      v-bind="props"
      variant="outlined"
      size="small"
      color="primary"
    >
      {{ title }}
    </v-btn>

  </template>

  <v-card
  >
    <v-card-title
    >
      <v-row
        :no-gutters="true"
      >
        <v-col>
          {{ title }}
        </v-col>
        <v-col
            cols="2"
            class="d-flex justify-center align-center"
        >
          <v-icon
              :color="color.hex"
              icon="mdi-circle"

          />
        </v-col>
        <v-col
            cols="1"
            class="d-flex justify-center align-center"
        >
          <app-icon-btn
            icon="mdi-close-thick"
            @click="menu=false"
          ></app-icon-btn>
        </v-col>
      </v-row>

    </v-card-title>
    <v-card-text>

      <v-row
        class="justify-center"
        :no-gutters="true"
      >
        <iro-color-picker
            :options="options"
            :color="color.hex"
            @color:change="changeColor"
            @input:end="updateColor"
        />
      </v-row>
      <v-row
          :no-gutters="true"
          class="mt-4 justify-space-between"
      >
        <v-col
            class="color-input ms-2"
        >
          <v-text-field
              v-model.number="color.rgb.r"
              @update:model-value="(newValue) => changeChannel(newValue, 'r')"
              density="compact"
              :hide-details="true"
              variant="outlined"

          />
          <div>{{ $t('settings.ui.colors.r') }}</div>
        </v-col>
        <v-col
            class="color-input ms-2"
        >
         <v-text-field
             v-model.number="color.rgb.g"
             @update:model-value="(newValue) => changeChannel(newValue, 'g')"
             density="compact"
             :hide-details="true"
             variant="outlined"

         />
          <div>{{ $t('settings.ui.colors.g') }}</div>
        </v-col>
        <v-col
          class="color-input ms-2"
        >
          <v-text-field
              v-model.number="color.rgb.b"
              @update:model-value="(newValue) => changeChannel(newValue, 'b')"
              density="compact"
              :hide-details="true"
              variant="outlined"
          />
          <div>{{ $t('settings.ui.colors.b') }}</div>
        </v-col>

      </v-row>
    </v-card-text>
  </v-card>

</v-menu>
</template>

<style scoped lang="scss">

.color-input div{
    text-align: center;
}


</style>