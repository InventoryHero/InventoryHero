<script lang="ts">
import {defineComponent} from 'vue'

// PRETTY MUCH TAKEN FROM
// https://github.com/fluidd-core/fluidd/blob/develop/src/components/ui/AppSetting.vue



export default defineComponent({
  name: "AppSetting",
  props: {
    rCols: {
      type: Number,
      default: 6
    },
    title: {
      type: String,
      default: ""
    },
    subTitle: {
      type: String,
      default: ""
    }
  },
  computed:{
    cols(){
      return [12-this.rCols, this.rCols]
    },
    subTitleSet(){
      return this.$slots['subTitle'] !== undefined || this.subTitle !== ""
    },
    subTitle2Set(){
      return this.$slots['subTitle2'] !== undefined || this.subTitle !== ""
    }
  }
})
</script>

<template>
  <v-row
    :no-gutters="true"
    class="setting"
  >
    <v-col
      :cols="cols[0]"
      class="setting-title"
      align-self="center"
    >
      <slot name="title">
        {{ title }}
      </slot>
      <div
        v-if="subTitleSet"
        class="setting-sub-title secondary--text"

      >
        <slot name="subTitle">
          {{ subTitle }}
        </slot>
      </div>

    </v-col>
    <v-col
      :cols="cols[1]"
      class="controls"
      align-self="center"
    >
      <slot></slot>
    </v-col>
  </v-row>
  <v-row class="setting mt-0" :no-gutters="true" v-if="subTitle2Set">
    <slot name="subTitle2">
      {{ subTitle }}
    </slot>
  </v-row>

</template>

<style scoped lang="scss">





.setting {
  // align-items: center;
  display: flex;
  flex: 1 1 100%;
  letter-spacing: normal;
  min-height: 48px;
  outline: none;
  padding: 0 16px;
  position: relative;
  text-decoration: none;
}

.setting > .col {
  padding: 12px 0;
}

.col.setting-title {
  // display: flex;
  // flex: 0 1 auto;
  // justify-content: space-between;
  // align-items: center;
  padding-top: 12px;
  padding-bottom: 12px;
  padding-right: 12px;
}

.col.setting-title > .setting-sub-title {
  font-size: 0.875rem;
}

.setting__link {
  cursor: pointer;
  user-select: none;
}

.setting__link:hover::before {
  opacity: 0.08;
}

.setting__link::before {
  background-color: currentColor;
  bottom: 0;
  content: "";
  left: 0;
  opacity: 0;
  pointer-events: none;
  position: absolute;
  right: 0;
  top: 0;
  transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.controls {
  display: inline-flex;
  align-self: center;
  justify-content: flex-end;
  align-items: center;


}

</style>