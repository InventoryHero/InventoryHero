<script lang="ts">
import {defineComponent, PropType} from 'vue'


import {type Product, ProductLocations, StorageTypes} from "@/types";
import ProductDetailCard from "@/components/products/ProductDetailCard.vue";
import AppConfirmModalActivatorBtn from "@/components/ui/AppModalActivatorBtn.vue";
import useNewAxios from "@/composables/useNewAxios.ts";
import {ProductEndpoint} from "@/api/http";

export default defineComponent({
  name: "ProductOverlay",
  components: {AppConfirmModalActivatorBtn, ProductDetailCard},
  setup(){
    const {axios} = useNewAxios("product")
    return {axios: axios as ProductEndpoint}
  },
  emits:{
    'update:modelValue'(payload: Product | undefined){
      return true
    },
    deleted(payload: number|undefined){
      return true;
    },
    updated(payload: Product){
      return true;
    },
    updateMapping(mapping: ProductLocations, callback: () => void){
      return true;
    },
    deleteMapping(productId: number, callback: () => void){
      return true;
    }
  },
  computed:{
    locations(): Array<ProductLocations>{
      return this.storageLocations
    },
    visible:{
      get(): boolean{
        return this.product !== undefined
      },
      set(value: boolean){
        if(!value)
        {
          this.$emit('update:modelValue', undefined)
        }

      }
    },
    product(){
      return this.modelValue
    },
    productName: {
      get(): string{
        if(this.newName !== undefined)
          return this.newName
        return this.product?.name ?? ''
      },
      set(value: string)
      {
        this.newName = value
      }
    }
  },
  props: {
    modelValue: {
      type: Object as PropType<Product> | undefined,
      default: undefined
    },
    storageLocations:{
      type: Array<ProductLocations>,
      default: []
    }
  },
  data(){
    return {
      deleteClicked: false,
      saveClicked: false,
      deleting: false,
      saving: false,
      edit: false,
      newName: undefined as undefined|string,
      rules: {
        not_empty: (value: string) => value !== '' || this.$t('products.product.rules.new_name_empty')
      },
      mappingOverlay: undefined as undefined|ProductLocations
    }
  },
  methods: {
    toggleEdit(event: boolean)
    {
      this.edit=event
      if(!this.edit)
      {
        this.newName = undefined
      }
    },
    async handleDelete(event: string){
      if(event === "deny"){
        return false
      }
      this.deleting=true
      let success = await this.axios.deleteProduct(this.product?.id ?? null)
      this.deleting = false
      if(success){
        this.visible=false
        this.$notify({
          title: this.$t('toasts.titles.success.deleted_product'),
          text: this.$t('toasts.text.success.deleted_product'),
          type: "success"
        })
        this.$emit('deleted', this.product!.id)
      }
      return success
    },
    async handleSave(event: string)
    {

      if(event === "deny"){
        return false
      }

      if(this.newName === this.product?.name){
        return true
      }
      if(this.newName === '')
      {
        // TODO NOTIFY
        return false
      }
      this.saving = true
      let {success, product} = await this.axios.updateProduct(this.product?.id ?? null, {
        name: this.newName
      })
      this.saving = false
      if(success){
        this.$emit('updated', product!)
        this.$notify({
          title: this.$t('toasts.titles.success.updated_product'),
          text: this.$t('toasts.text.success.updated_product'),
          type: "success"
        })
      }
      // TODO NOTIFICATION
      return success
    },
    async eventHandler(event: string, type: string, callback: () => void){
      switch(type)
      {
        case "delete":
          this.deleteClicked = false
          await this.handleDelete(event)
          this.deleting = false

          break;
        case "save":
          this.saveClicked = false
          await this.handleSave(event)
          //this.saving = false
          break
      }
      callback()
    },
    async updateMapping(mapping: ProductLocations, update: Partial<ProductLocations>, callback: () => void){
      const {success, updated, deleted} = await this.axios.updateProductAt(mapping.id, update)
      if(!success)
      {
        this.$emit('updateMapping', mapping, callback)
        return false;
      }
      // TODO NOTIFICATION LOCALIZATION
      this.$notify({
        title: this.$t('toasts.titles.success.updated_detail'),
        text: this.$t('toasts.text.success.updated_detail'),
        type: "success"
      })
      this.$emit('updateMapping', updated!, callback)

      if(updated!.id === this.mappingOverlay?.id)
      {
        this.mappingOverlay = updated
      }

      if(deleted === undefined)
      {
        return true;
      }
      this.$emit('deleteMapping', deleted.product_id, () => {
        if(this.mappingOverlay?.id === deleted.id)
        {
          this.mappingOverlay = updated
        }
      })
    },
    async deleteMapping(id: number, product_id: number, callback: () => void){
      let success = await this.axios.deleteProductAt(id)

      if(!success){
        this.$emit('deleteMapping', id, callback)
        return
      }

      this.$emit('deleteMapping', product_id, callback)
      this.$notify({
        title: this.$t('toasts.titles.success.deleted_detail'),
        text: this.$t('toasts.text.success.deleted_detail'),
        type: "success"
      })
      if(this.mappingOverlay?.id === id)
      {
        this.mappingOverlay = undefined
      }
    },
    showMappingOverlay(item: ProductLocations)
    {
      this.mappingOverlay = item
    },
    redirect(storage: Storage, from: string)
    {
      if(storage === null)
        return
      switch(storage?.type ?? -1){
        case StorageTypes.Location:
          return this.$router.push("/storage/locations/" + storage.id + "/" + this.$t('product', {name: this.productName}))
        case StorageTypes.Box:
          return this.$router.push("/storage/boxes/" + storage.id + "/" + this.$t('product', {name: this.productName}))
        default:
          return
      }
    }
  }
})
</script>

<template>
  <product-detail-overlay
    v-model="mappingOverlay"
    :product-name="productName"
    @redirect-to-storage="redirect"
    @product-mapping:update="updateMapping"
    @product-mapping:delete="deleteMapping"
  />


  <detail-overlay
      v-model="visible"
      @toggle-edit="toggleEdit($event)"
      @deny="(event: 'save'|'delete', callback: () => void) => eventHandler('deny', event, callback)"
      @accept="(event: 'save'|'delete', callback: () => void) => eventHandler('accept', event, callback)"
  >
      <template #title>
        <app-overlay-title
            v-model="productName"
            :rules="[rules.not_empty]"
            :edit="edit"
        />

      </template>
      <RecycleScroller
          :items="locations"
          :item-size="110"
          style="height: 100%;"
      >
        <template #default="{item}">
          <product-detail-card
              :item="item"
              :product-name="productName"
              @product-mapping:update="updateMapping"
              @product-mapping:delete="deleteMapping"
              @show-mapping-overlay="showMappingOverlay"
              @redirect-to-storage="redirect"
          />
        </template>
        <template #after>
          <v-row
              :no-gutters="true"
              justify="center"
          >
            <p class="text-center">
              {{ $t("products.locations.all_displayed")}}
            </p>
          </v-row>
        </template>
      </RecycleScroller>

      <template v-slot:delete-confirm="del">
        <app-confirm-modal
          @deny="del.deny()"
          @accept="del.accept()"
          :dialog="del.active"
          :no-click-animation="true"
          :title="$t('products.confirm.product.delete.title')"
          :body="$t('products.confirm.product.delete.body')"
        />
      </template>
      <template v-slot:save-confirm="save">
        <app-confirm-modal
            @deny="save.deny()"
            @accept="save.accept()"
            :dialog="save.active"
            :no-click-animation="true"
            :title="$t('products.confirm.product.save.title')"
            :body="$t('products.confirm.product.save.body')"
        />
      </template>
  </detail-overlay>


</template>

<style scoped lang="scss">


</style>