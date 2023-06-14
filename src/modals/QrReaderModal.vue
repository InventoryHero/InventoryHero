<template>
    <v-dialog
        transition="dialog-bottom-transition"
        width="auto"
    >
        <v-card
            height="100%"
            class="d-flex-column modal-container"
        >
            <v-toolbar
                title="test"
                class="toolbar"
            >
                <v-icon class="me-5" icon="fa:fas fa-times" @click="closeModal()"></v-icon>
            </v-toolbar>
            <v-card-text>
                <qrcode-stream @decode="onDecode"></qrcode-stream>
            </v-card-text>
        </v-card>

    </v-dialog>
</template>

<script>
import {QrcodeStream} from "vue-qrcode-reader/src";

export default {
    name: 'App',
    props: {

    },
    components: {
        QrcodeStream

    },
    data() {

    },
    methods: {
        onDecode(decodedString)
        {
            this.$emit('loadDetailView', JSON.parse(decodedString));
        },
        closeModal()
        {
            console.log("HI");
            this.$emit('closeQrModal')
        }

    },
    beforeMount() {

    }
}
</script>

<style scoped>
#mainContainerAddModal {
    position: absolute;
    top: 20vh;
    left: 5vw;
    right: 5vw;
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(15px);
    border-radius: 10px;
    border: white solid 1px;
    height: 60vh;
}

#exitButton {
    position: absolute;
    right: 10px;
    top: 10px;
    fill: white;
    border: 1px solid white;
    border-radius: 10px;
    cursor: pointer;
}

#addWhat {
    position: absolute;
    display: flex;
    top: 10vh;
    left: 50%;
    transform: translateX(-50%);
}

#containerWhat {
    position: absolute;
    top: 17vh;
    left: 5%;
    bottom: 10px;
    width: 90%;
}

.addButton {
    position: absolute;
    bottom: 10px;
}
</style>
  