<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Storage, Product} from "@/types";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";


export default defineComponent({
  name: "DetailOverlay",
  components: {FontAwesomeIcon},
  mounted(){
    this.$emitter.on('nav-opened', () => {
      this.model=false
    })
  },
  emits: {
    toggleEdit(value: boolean){
      return true
    },
    'update:modelValue'(payload: boolean){
      return true
    },
    deny(type: 'save'|'delete', callback: () => void){
      return !(type !== "save" && type !== "delete");

    },
    accept(type: 'save'|'delete', callback: () => void){
      return !(type !== "save" && type !== "delete");

    }
  },
  watch:{
    saveClicked(){
      if(this.saveClicked && !this.saveConfirmModalSet){
        this.accept('save')
      }
    },
    deleteClicked(){
      if(this.deleting && !this.deleteConfirmModalSet){
        this.accept('delete')
      }
    }
  },
  computed:{
    model:{
      get(): boolean{
        return this.modelValue
      },
      set(value: boolean){
        this.editClicked = false
        this.$emit('update:modelValue', value)
      }
    },
    hasSubTitle(){
      return this.$slots['subTitle'] !== undefined || this.subTitle !== ''
    },
    saveConfirmModalSet(){
      return this.$slots['save-confirm'] !== undefined
    },
    deleteConfirmModalSet(){
      return this.$slots['delete-confirm'] !== undefined
    },
    titleCols(){
      return [this.titleLCols, 12-this.titleLCols]
    }
  },
  props: {
    modelValue: {
      type: Boolean,
    },
    title: {
      type: String,
      default: ""
    },
    subTitle: {
      type: String,
      default: ""
    },
    titleLCols: {
      type: Number,
      default: 10
    },
    loading: {
      type: Boolean,
      default: false
    },
  },
  data(){
    return {
      editClicked: false,
      saveClicked: false,
      deleteClicked: false,
      saving: false,
      deleting: false,
    }
  },
  methods:{
    clickEditBtn(){
      this.editClicked = true
      this.$emit('toggleEdit', this.editClicked)
    },
    closeEdit(){
      this.editClicked=false
      this.saving = false
      this.deleting = false
      this.$emit('toggleEdit', false)
    },
    deny(event: "save"|"delete"){
      this.$emit('deny', event, this.closeEdit)
      this.saveClicked = false
      this.deleteClicked = false
    },
    accept(event: "save"|"delete"){
      switch(event){
        case "save":
          this.saving = true
          break
        case "delete":
          this.deleting = true
          break
      }
      this.$emit('accept', event, this.closeEdit)
      this.saveClicked = false
      this.deleteClicked = false
    },
    minimize(){
      this.closeEdit()
      this.model = false
    }
  }
})
</script>

<template>
  <v-dialog
      v-model="model"
      :contained="true"
      content-class="detail-dialog pa-0 ma-0"
      :persistent="true"
      :no-click-animation="true"
      :scrim="false"
      :fullscreen="true"
  >
    <v-card
      class="position-relative d-flex flex-column fill-height"
    >
      <v-progress-linear
        :indeterminate="true"
        :active="loading"
        color="primary"
      />
      <v-card-title
        class="d-flex align-center justify-space-between"
      >
        <slot name="title">
          {{ title }}
        </slot>

        <div
          class="ms-4"
        >
          <v-btn
              density="compact"
              icon="fa:fas fa-edit"
              variant="flat"
              size="small"
              class="me-2"
              @click="clickEditBtn()"
          >
            <template v-slot:default>
              <v-icon :color="editClicked ? 'primary' : ''"></v-icon>
            </template>
          </v-btn>
          <v-btn
              density="compact"
              icon="fa:fas fa-window-minimize"
              variant="flat"
              size="small"
              @click="minimize()"
          >
          </v-btn>
        </div>
      </v-card-title>
      <v-card-subtitle v-if="hasSubTitle" >
        <slot name="subTitle"
          class="hallo-christian"
        >
          {{ subTitle }}
        </slot>
      </v-card-subtitle>


      <v-card-text class="flex-1-1 pt-0 pl-4 pr-4 overflow-hidden">
          <slot />
      </v-card-text>
      <v-card-actions
          v-if="editClicked"
          class="d-flex justify-end"
      >
        <v-btn
            prepend-icon="fa:fas fa-cancel"
            @click="closeEdit()"
            :text="$t('cancel')"
        />
        <app-modal-activator-btn
            icon="fa:fas fa-trash"
            :loading="deleting"
            :title="$t('delete')"
            v-model="deleteClicked"
        />
        <app-modal-activator-btn
            icon="fa:fas fa-save"
            :loading="saving"
            v-model="saveClicked"
            :title="$t('save')"
        />

        <slot
            name="delete-confirm"
            :active="deleteClicked"
            :deny="() => {deny('delete')}"
            :accept="() => {accept('delete')}"
        />
        <slot
            name="save-confirm"
            :active="saveClicked"
            :deny="() => {deny('save')}"
            :accept="() => {accept('save')}"
        />

      </v-card-actions>
    </v-card>

  </v-dialog>

</template>

<style lang="scss">


</style>