<template>
    <SandwichMenu :title="this.title"/>
    <search-bar @valueUpdated="sortLocations"/>

    <RoomCard
        v-for="r in this.rooms"
        @addItemToRoom="displayModal"
        @roomDeleted="updateRooms"
        class="card"
    :key="r.id"
    :id="r.id" 
    :roomName="r.name" 
    :numBoxes="r.box_cnt" 
    :numProducts="r.product_cnt" />
    <load-animation v-if="this.loading"></load-animation>
    <div id="spacing"></div>
    <add-modal
        :preselected_room="this.preselectedRoom"
        :navbarItems="this.displayedNavbarItems"
        :defaultAddView="this.defaultModalView"
        v-model="this.addModalVisibility"
        @closeModal="closeModal()"
    />

    <dock
        :show_qr="false"
        @addButton="this.addModalVisibility = true"
    />
</template>

<script>
import RoomCard from "@/components/RoomCard.vue";
import SandwichMenu from "@/components/SandwichMenu.vue";
import LoadAnimation from "@/components/LoadAnimation.vue";
import SearchBar from '@/components/SearchBar.vue';
import Dock from "@/components/Dock.vue";


import AddModal from "@/modals/AddModal.vue";


import { DB_SB_delete_room, DB_SB_get_room_name, DB_SB_get_rooms, DB_SB_getStarredProducts} from '@/db/supabase';
import { getUser } from "@/db/dexie";
import { Constants } from "@/global/constants";
import { rankLocationsBySearch } from '@/scripts/sort';
import QrDataModal from "@/modals/QrDataModal.vue";
import QrReaderModal from "@/modals/QrReaderModal.vue";
import {useToast} from "vue-toastification";



  
  export default {
    name: 'App',
    setup(){
        const toast = useToast();
        return {toast};
    },
    components: {
        QrReaderModal, QrDataModal,
        Dock,
        LoadAnimation,
        AddModal,
        RoomCard,
        SandwichMenu,
        SearchBar
    },
    data() {
        return {
            rooms: [],
            currentUser: "",
            addModalVisibility: false,
            Constants,
            title: "Locations",
            defaultModalView: Constants.LocationsView,
            displayedNavbarItems: Constants.All,
            preselectedRoom: "",
            loading: true
        }
    },
    methods: {
        async updateRooms(id)
        {
            document.getElementById(id).setAttribute("hidden", true);
            if(!await DB_SB_delete_room(id)){
                this.toast.error("Failed to delete room");
                return;
            }
            this.toast.success("Deleted room successfully");
            await this.get_rooms()
        },
        displayRoomDetailView(id){
          console.warn("I should display the detail view modal " + id);
        },
        displayModal(id){
            DB_SB_get_room_name(id).then((room) => {
                this.preselectedRoom = room;
                this.defaultModalView = Constants.ProductsView;
                this.displayedNavbarItems = [Constants.ProductsView, Constants.BoxesView];
                this.addModalVisibility = true;
            })
        },
        async get_rooms() {
            const locations = await DB_SB_get_rooms(this.currentUser.username)
            this.rooms = rankLocationsBySearch(locations, "");
            this.loading = false;
            return locations
        },
        closeModal() {
            this.addModalVisibility = false;
            this.defaultModalView = Constants.LocationsView;
            this.displayedNavbarItems = Constants.All;
            this.preselectedRoom = "";
            this.get_rooms();
            DB_SB_getStarredProducts().then((res) => {
                this.starred_products = res;
            })
        },
        async sortLocations(search_word) {
            const locations = await this.get_rooms();
            this.rooms = rankLocationsBySearch(locations, search_word);
        }
    },
    beforeMount() {
        getUser().then((user) => {
            if(user === undefined)
            {
                this.$router.push("/login");
            }
            this.currentUser = user;
            this.get_rooms();
        });
    }

  }
</script>
  
<style scoped>
    .card {
        padding-left: 2.5%;
        padding-right: 2.5%;
    }
    .v-virtual-scroll{
        background: var(--color-blue);
    }
    #spacing{
        height: calc(5vh + 25px);
    }
    ::-webkit-scrollbar { width: 0px;  }
</style>
  