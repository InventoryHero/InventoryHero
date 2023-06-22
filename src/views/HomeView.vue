<template>
  <div class="list-padding" id="posStarredMessages">
      <v-card class="dark-theme card">
        <v-card-title align="start">
          {{this.$t('home_view.starred_products')}}
        </v-card-title>
        <v-list class="scroll dark-theme">
          <usage-component 
            v-for="p in starredProducts" 
            :id="p.id"
            :mapping_id="p.mapping_id"
            :productName="p.name"
            :amount="p.amount"
            :updated_at="p.updated_at"
            :room_id="p.room_id"
            :box_id="p.box_id"
            :box_name="p.box_name"
            :room_name="p.room_name"
            @productDeleted="deleteProduct"
            @reloadProducts="refreshData"
          />
      </v-list>
      </v-card>
    </div>

    <div class="list-padding" id="posLastUsed">
      <v-card class="dark-theme card">
        <v-card-title align="start">
          {{this.$t('home_view.last_used')}}
                </v-card-title>
        <v-list class="scroll dark-theme">
        <usage-component
          v-for="p in lastUsedProducts" 
          :id="p.id"
          :mapping_id="p.mapping_id"
          :productName="p.name"
          :amount="p.amount"
          :updated_at="p.updated_at"
          :room_id="p.room_id"
          :box_id="p.box_id"
          :box_name="p.box_name"
          :room_name="p.room_name"
          @productDeleted="deleteProduct"
          @reloadProducts="refreshData"
        />
      </v-list>
      </v-card>
    </div>

  <add-modal v-model="this.addModalVisibility" @closeModal="closeModal()"/>
  <qr-reader-modal
          v-model="this.qrReaderModalVisibility"
          @closeQrModal="closeQrModal()"
          @loadDetailView="loadDetailView"
  />
  <qr-data-modal
          v-model="this.qrCodeDataModalVisibility"
          v-bind:qr-code-data="this.qrCodeData"
          @closeQrDataModal="this.qrCodeDataModalVisibility=false"

  />
  <dock
    @qrButton="this.qrReaderModalVisibility=true"
    @addButton="this.addModalVisibility = true"
  />
  <SandwichMenu :title="this.$t('home')"/>

</template>

<script>
import SandwichMenu from "@/components/SandwichMenu.vue";
import ListContainer from '@/components/ListContainer.vue';
import UsageComponent from '@/components/UsageComponent.vue';
import AddModal from '@/modals/AddModal.vue';
import QrReaderModal from "@/modals/QrReaderModal.vue";
import QrDataModal from "@/modals/QrDataModal.vue";
import Dock from "@/components/Dock.vue";
import { DB_SB_getStarredProducts } from '@/db/supabase';
import { DB_SB_getLastUsedProducts } from '@/db/supabase';
import {getSettings, getUser} from "@/db/dexie";

export default {
  name: 'App',
  components: {
    SandwichMenu,
    ListContainer,
    UsageComponent,
    AddModal,
    QrReaderModal,
    QrDataModal,
    Dock
  },
  data() {
    return {
      currentUser: "",
      showTitle: true,
      starred_products: [],
      addModalVisibility: false,
      qrReaderModalVisibility: false,
      qrCodeDataModalVisibility: false,
      qrCodeData: Object,
      lastUsedProducts: [],
      starredProducts: [],
      theme: "",
    }
  },
  methods: {
    deleteProduct()
    {
      this.refreshData();
    },
    refreshData(){
      this.data_changed = true;
      this.get_products();
    },
    closeQrModal()
    {
      this.qrReaderModalVisibility = false;
    },
    loadDetailView(qr_data)
    {
      this.qrCodeData = qr_data;
      this.qrReaderModalVisibility = false;
      this.qrCodeDataModalVisibility = true;
    },
    closeModal() {
      this.addModalVisibility = false;
      DB_SB_getStarredProducts().then((res) => {
        this.starred_products = res;
      })
    },
    async get_products() {
        this.lastUsedProducts = await DB_SB_getLastUsedProducts(this.currentUser.username);
        this.starredProducts = await DB_SB_getStarredProducts(this.currentUser.username);
        this.loading = false;
      },
    
  },
  
  beforeMount() {
    getUser().then((user) => {
      if(user === undefined)
      {
        this.$router.push("/");
      }
    });
    DB_SB_getStarredProducts().then((res) => {
      this.starred_products = res;
    })
    getSettings().then((settings) => {
      this.theme =  settings.theme;
    }),
    getUser().then((user) => {
      if(user === undefined)
      {
        this.$router.push("/login");
      }
      this.currentUser = user;
      this.get_products();
    });
    
  }
}
</script>

<style scoped>
#posStarredMessages {
  margin-top: 15vh;
  width: 100%;
  word-wrap: break-word;
}

#posLastUsed {
  margin-top: 5vh;
    word-wrap: break-word;
}


h3 {
  text-align: left;
  margin-left: 10%;
}
.dark-theme  {
  background-color: var(--color-dark-theme-darker);
  color: white;
}

.list-padding {
  padding-left: 12.5%;
  padding-right: 12.5%;
}

.scroll {
    overflow-y: scroll;
    height: 26vh;
}

</style>
