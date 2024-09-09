<script lang="ts">
import {defineComponent} from 'vue'
import {ApiStorage} from "@/types";

type Paper = {
  height: number,
  width: number
}


const papers = {
  "A4": {
    height: 297,
    width: 210,
  }
}


export default defineComponent({
  name: "AppPrintPreview",
  computed:{
    items(){
      let rows = [] as Array<Array<ApiStorage>>
      for(let i = 0; i < this.modelValue.length; i++)
      {
        if(i % this.itemsPerRow === 0)
        {
          rows.push([] as Array<ApiStorage>)
        }
        rows[rows.length-1].push(this.modelValue[i])

      }
      return rows
    },
    paperHeight(){
      return papers[this.paper].height;
    },
    paperWidth(){
      return papers[this.paper].width;
    },
    margin(){
      return {
        bottom: `${this.marginBottom}mm`,
        top: `${this.marginTop}mm`,
        right: `${this.marginRight}mm`,
        left: `${this.marginLeft}mm`,
      }
    }
  },
  props:{
    modelValue: {
      type: Array<Storage>,
      default: []
    },
    paper: {
      type: String,
      default: "A4"
    },
    itemsPerRow: {
      type: Number,
      default: 3
    },
    showTitle:{
      type: Boolean,
      default: true
    },
    showStorageTypeIcon: {
      type: Boolean,
      default: true
    },
    printLabel: {
      type: Boolean,
      default: true
    },
    marginTop: {
      type: Number,
      default: 10
    },
    marginBottom: {
      type: Number,
      default: 10
    },
    marginRight: {
      type: Number,
      default: 10
    },
    marginLeft: {
      type: Number,
      default: 10
    },
    qrCodeIcon:{
      type: Boolean,
      default: true
    }

  }
})
</script>

<template>
  <v-sheet
    class="page"
    :style="`height: ${paperHeight}mm; width: ${paperWidth}mm`"

  >
    <div class="content">
      <div
          v-for="row in items"
          class="row d-flex"
      >
        <div
            v-for="col in row"
            class="col"
        >
          <app-storage-qr-code
              :storage="col"
              :show-storage-type-icon="showStorageTypeIcon"
              :show-title="showTitle"
              :print-label="printLabel"
              :show-qr-code-icon="qrCodeIcon"
          />
        </div>
      </div>
    </div>
  </v-sheet>
</template>

<style scoped lang="scss">
.page{
  background-color: white;
  color: black;

  .content{
    margin: v-bind('margin.top') v-bind('margin.right') v-bind('margin.bottom') v-bind('margin.left');
    .row{

      .col{
        width: calc((1 / v-bind(itemsPerRow)) * 100% - 8px);
        margin-right: 8px;
      }
    }
  }
}

</style>