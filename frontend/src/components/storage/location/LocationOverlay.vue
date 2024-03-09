<script lang="ts">
import {defineComponent, PropType, ref} from 'vue'
import {type Box, ProductLocations, ProductOnly, isInstanceOfStorage, Location, LocationContent} from "@/types";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import useUpdateStorage from "@/composables/useUpdateStorage";
import useNewAxios from "@/composables/useNewAxios.ts";
import {LocationEndpoint, ProductEndpoint} from "@/api/http";





export default defineComponent({
  name: "LocationOverlay",
  components: {FontAwesomeIcon},
  setup() {
    const {axios} = useNewAxios('location');
    const productEndpoint = useNewAxios('product')
    return {
      axios: axios as LocationEndpoint,
      productEndpoint: productEndpoint.axios as ProductEndpoint
    }
  },
  emits:{
    'update:modelValue'(payload: Partial<Location>){
      return true;
    },
    boxMoved(){
      return true;
    },
    boxDeleted(){
      return true;
    },
    deleted(){
      return true
    },
    updated(payload: Location|undefined){
      return true
    },
    contentChanged(locaationId: number, newLocationId: number|undefined){
      return true
    }
  },
  watch: {
    location(newVal){
      if(newVal !== undefined)
      {
        this.loadContent()
      }
      else
      {
        this.overlayBox = undefined
        this.content = []
      }

    }
  },
  computed:{
    locationContent() {
      return this.content
    },
    location(){
      return this.modelValue
    },
    visible:{
      get(): boolean{
        return this.modelValue !== undefined && this.modelValue !== null
      },
      set(value: boolean){
        this.$emit('update:modelValue', undefined)
        if(!value)
        {
          this.reset()
        }
      }
    },
    name:{
      get(): string{
        if(this.newName !== undefined)
        {
          return this.newName
        }
        return this.location?.name ?? ''
      },
      set(value: string){
        this.newName = value
      }
    },
    overlayProductName(){
      return this.overlayProduct?.name ?? ''
    },
  },
  props: {
    modelValue: {
      type: Object as PropType<Location> | undefined,
      default: undefined
    }
  },
  data(){
    return {
      contentLoading: false,
      content: [] as Array<LocationContent>,
      overlayBox: undefined as Box|undefined,
      deleting: false,
      saving: false,
      newName: undefined as undefined|string,
      rules:{
        not_empty: (value: string) => value !== '' || this.$t('locations.location.rules.new_name_empty')
      },
      edit: false,
      saveClicked: false,
      deleteClicked: false,
      overlayProduct: undefined as ProductLocations|undefined
    }
  },
  methods:{
    reset()
    {
      Object.assign(this.$data, this.$options.data.apply(this))
    },
    async loadContent(){
      this.contentLoading = true
      const {boxes, products} = await this.axios.getContent(this.location?.id ?? '')

      this.content = []
      boxes.forEach((box) => {
        this.content.push({
          content: box,
          type: "box",
          id: `box${box.id}`
        })
      })
      products.forEach((product) => {
        this.content.push({
          content: product,
          type: "product",
          id: `product${product.id}`
        })
      })
      this.contentLoading = false
    },
    isBox(item: LocationContent) {
      return item.type === "product"
    },
    updateBox(toUpdate: Box){
      if(toUpdate.location?.id !== this.location?.id)
      {
        this.overlayBox = undefined;
        this.loadContent();
        this.$emit('boxMoved')
        return
      }

      if(this.overlayBox?.id === toUpdate.id)
      {
        this.overlayBox = toUpdate
      }
      let i = 0;
      for(; i < this.content.length; i++)
      {
        if(this.content[i].id === `box${toUpdate.id}`){
          this.content[i].content.name = toUpdate.name
          let current: Box = this.content[i].content as Box
          current.location = toUpdate.location
        }
      }
    },
    deleteBox(){
      this.content = this.content.filter((item) => item.id !== `box${this.overlayBox?.id}`)
      this.overlayBox = undefined
      this.$emit("boxDeleted")
    },
    async handleDelete(event: string){
      if(event === "accept")
      {
        this.deleting=true
        let success = await this.axios.deleteStorage(this.location?.id ?? null)
        this.deleting=false
        if(success)
        {
          this.visible = false
          this.$notify({
            title: this.$t('toasts.titles.success.deleted_location'),
            text: this.$t('toasts.text.success.deleted_location'),
            type: "success"
          })
          this.$emit('deleted')
          return true
        }
        return false
      }
    },
    async handleSave(event: string)
    {
      if(event === "deny")
      {
        return false
      }
      // TODO EMPTY NAMES SHOULD NOT BE ALLOWED EVEN WHEN RENAMING!!!!
      this.saving = true
      let result = await this.axios.updateLocation(this.location?.id ?? null, {
        name: this.name
      })
      this.saving = false;
      if(result !== undefined)
      {

        this.$emit('updated', result.updated)
        this.$notify({
          title: this.$t('toasts.titles.success.updated_location'),
          text: this.$t('toasts.text.success.updated_location'),
          type: "success"
        })
      }
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
          this.saving = false
          break
      }

      callback()
    },
    toggleEdit(event: boolean)
    {
      this.edit=event
      if(!this.edit)
      {
        this.newName = undefined
      }
    },
    async deleteProduct(id: number, product_id: number, callback: () => void) {

      let success = await this.productEndpoint.deleteProductAt(id)

      if (success) {
        this.$notify({
          title: this.$t('toasts.titles.success.deleted_detail'),
          text: this.$t('toasts.text.success.deleted_detail'),
          type: "success"
        })
        this.loadContent()
        this.$emit('contentChanged', this.location?.id)
      }
      callback()
      this.overlayProduct = undefined
    },
    async updateProduct(mapping: ProductLocations, update: Partial<ProductLocations>, callback: () => void) {
      const {success, updated, deleted} = await this.productEndpoint.updateProductAt(mapping.id, update)

      callback()
      if(!success)
      {

        return false;
      }
      this.products = []
      this.loadContent()
      this.$notify({
        title: this.$t('toasts.titles.success.updated_detail'),
        text: this.$t('toasts.text.success.updated_detail'),
        type: "success"
      })
      if(
          deleted !== undefined ||
          updated!.id !== this.overlayProduct?.id ||
          updated!.storage?.id !== this.location?.id
      )
      {
        this.$emit('contentChanged', this.location?.id, updated?.storage?.id)
        this.overlayProduct = undefined
      }
    }
  }
})
</script>

<template>
  <box-overlay
      v-model="overlayBox"
      @deleted="deleteBox()"
      @updated="updateBox($event)"
  />

  <product-detail-overlay
      v-model="overlayProduct"
      :product-name="overlayProductName"
      :disable-storage-title="true"
      @product-mapping:delete="deleteProduct"
      @product-mapping:update="updateProduct"

  />

  <detail-overlay
      @toggle-edit="toggleEdit($event)"
      v-model="visible"
      :loading="contentLoading"
      @deny="(event: 'save'|'delete', callback: () => void) => eventHandler('deny', event, callback)"
      @accept="(event: 'save'|'delete', callback: () => void) => eventHandler('accept', event, callback)"

  >
    <template #title>
      <app-overlay-title
          v-model="name"
          :rules="[rules.not_empty]"
          :edit="edit"
      />
    </template>

    <RecycleScroller
        :items="locationContent"
        :item-size="110"
    >

      <template #default="{item}">
        <product-card
            v-if="isBox(item)"
            :id="item.content.id"
            :name="item.content.name"
            :totalAmount="item.content.amount"
            :creation-date="item.content.updated_at"
            :is-updated-date="true"
            @expand="overlayProduct = {
              ...item.content,
              storage: location
            }"
        />
        <box-card
          v-else
          :id="item.content.id"
          :name="item.content.name"
          :creation-date="item.content.creation_date"
          @show-overlay="() => {overlayBox = item.content}"
        />

      </template>
      <template #after>
        <v-row
            :no-gutters="true"
            justify="center"
        >
          <p>
            {{ $t("locations.location.all_displayed")}}
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
          :title="$t('locations.confirm.delete.title')"
          :body="$t('locations.confirm.delete.body')"
      />
    </template>
    <template v-slot:save-confirm="save">
      <app-confirm-modal
          @deny="save.deny()"
          @accept="save.accept()"
          :dialog="save.active"
          :no-click-animation="true"
          :title="$t('locations.confirm.save.title')"
          :body="$t('locations.confirm.save.body')"
      />
    </template>
  </detail-overlay>
</template>

<style scoped lang="scss">

</style>