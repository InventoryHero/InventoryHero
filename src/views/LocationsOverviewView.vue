<template>
    <SandwichMenu :title="this.title"/>
    <v-virtual-scroll
        class="virtual-scroll-bg"
        :height="80+'vh'"
        :items="rooms"
    >
        <template v-slot:default="{ item }">
            <RoomCard
                @addItemToRoom="displayModal"
                @roomDeleted="updateRooms"
                class="card"
                :id="item.id"
                :roomName="item.name"
                :numBoxes="item.box_cnt"
                :numProducts="item.product_cnt"
                :username="this.currentUser.username"
            />
        </template>
    </v-virtual-scroll>
    <add-modal :preselected_room="this.preselectedRoom" :navbarItems="this.displayedNavbarItems" :defaultAddView="this.defaultModalView" v-if="this.addModalVisibility" @closeModal="closeModal()"/>
    <add-button @click="this.addModalVisibility = true"/>
    <qr-button/>
    <load-animation v-if="this.loading"></load-animation>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
  import QrButton from '@/components/QrButton.vue'
  import RoomCard from "@/components/RoomCard.vue";
import SandwichMenu from "@/components/SandwichMenu.vue";
//import RoomDetailModal from "@/modals/RoomDetailModal.vue";

import {DB_SB_delete_room, DB_SB_get_room_name, DB_SB_get_rooms, DB_SB_getStarredProducts} from '@/db/supabase';
import {getUser} from "@/db/dexie";
import AddModal from "@/modals/AddModal.vue";
import { Constants } from "@/global/constants";
import LoadAnimation from "@/components/LoadAnimation.vue";

  
  export default {
    name: 'App',
    components: {
        LoadAnimation,
        AddModal,
        RoomCard,
        AddButton,
        QrButton,
        SandwichMenu,
        //RoomDetailModal
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
            await DB_SB_delete_room(id);
            this.get_rooms()
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
        get_rooms() {
            DB_SB_get_rooms(this.currentUser.username).then((rooms) => {
                console.log(rooms);
                this.rooms = rooms;
                this.loading = false;
            });
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
    ::-webkit-scrollbar { width: 0px;  }
</style>
  