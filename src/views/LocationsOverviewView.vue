<template>
    <v-virtual-scroll
        class="virtual-scroll-bg"
        :height="80+'vh'"
        :items="rooms"
    >
        <template v-slot:default="{ item }">
            <RoomCard class="card" :id="item.id" :roomName="item.name" :numBoxes="item.box_cnt" :numProducts="item.product_cnt"/>
        </template>
    </v-virtual-scroll>
    <add-button/>
    <qr-button/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
  import QrButton from '@/components/QrButton.vue'
  import RoomCard from "@/components/RoomCard.vue";

  import { DB_SB_get_rooms } from '@/db/supabase';

  
  export default {
    name: 'App',
    components: {
        RoomCard,
        AddButton,
        QrButton
    },
    data() {
        return {
            rooms: [],
        }
    },
    methods: {
        get_rooms() {
            DB_SB_get_rooms().then((rooms) => {
                this.rooms = rooms;
            });
        }
    },
    beforeMount() {
        this.get_rooms();
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
  