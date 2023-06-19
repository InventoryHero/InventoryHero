<template>


    <v-dialog
        transition="dialog-bottom-transition"
        width="auto"
        persistent
        no-click-animation
        height="100%"
    >
        <v-card
            height="100%"
            class="d-flex-column modal-container"
        >
            <v-toolbar
                :title="this.$t('qr_reader_modal.title')"
                class="modal-toolbar"
            >
                <v-icon class="me-5" icon="fa:fas fa-times" @click="closeModal()"></v-icon>
            </v-toolbar>
            <v-card-text>
                <qrcode-stream  @decode="onDecode"  @init="logErrors" :track="this.paintBoundingBox"></qrcode-stream>
            </v-card-text>
        </v-card>

    </v-dialog>


</template>

<script>
import {QrcodeStream} from "vue-qrcode-reader/src";
import { useToast } from "vue-toastification";

export default {

    name: 'App',
    setup(){
      const toast = useToast();
      return {toast};
    },
    props: {
        model: Boolean

    },
    components: {
        QrcodeStream,


    },
    data() {
        return {
            barcodeInvalid: false,
        }
    },
    methods: {
        async onDecode(decodedString)
        {
            try{
                let data = JSON.parse(decodedString);

                if(!data.hasOwnProperty("id") || ! data.hasOwnProperty("is_room") || !data.hasOwnProperty("is_box") || !data.hasOwnProperty("username"))
                {
                    console.log(data);
                    this.toast.error(this.$t('qr_reader_modal.invalid_qr'));
                    return;
                }

                this.$emit('loadDetailView', data);
            }catch(e)
            {
                console.log(e);
                console.log("error while reading qr code");
            }

        },
        closeModal()
        {
            this.$emit('closeQrModal')
        },
        logErrors (promise) {
            promise.catch(console.error)
        },
        paintBoundingBox (detectedCodes, ctx) {
            for (const detectedCode of detectedCodes) {
                const { boundingBox: { x, y, width, height } } = detectedCode

                ctx.lineWidth = 2
                ctx.strokeStyle = '#007bff'
                ctx.strokeRect(x, y, width, height)
            }
        },

    },
    beforeMount() {

    }
}
</script>

<style scoped>




</style>
  