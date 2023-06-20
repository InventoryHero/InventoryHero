<template>
    <v-dialog
        transition="dialog-bottom-transition"
        width="100%"
        height="80%"
    >
        <div class="d-flex-column modal-container-sm">
            <v-toolbar
                class="modal-toolbar justify-content-end "
                :title="this.$t('confirmation_modal.delete')"
            >

                <v-spacer></v-spacer>
                <v-icon class="me-5" icon="fa:fas fa-times" @click="closeModal()"/>
            </v-toolbar>
            <v-card-text>
                <div class="scroll">
                    <p class="wrapMe">
                        {{ this.$t('confirmation_modal.delete_storage', {type: this.$t("confirmation_modal."+this.type), loc: this.name}) }}
                    </p>
                </div>

            </v-card-text>
            <v-card-actions class="justify-space-evenly">
                <v-btn
                    class="delete"
                    :text="this.$t('confirmation_modal.delete_'+this.type)"
                    @click="deleteContainer"
                />
            </v-card-actions>
        </div>

    </v-dialog>
</template>

<script>

export default {
name: 'App',
props: {
    name: "",
    type: "box",
},
components: {
},
data() {
    return {
    }
},
methods: {
    closeModal()
    {
        this.$emit("closeConfirmationModal");
    },
    deleteContainer()
    {
        this.$emit("deleteContainer");
    },
},
beforeMount() {
}
}
</script>

<style scoped>

.delete{
    background: rgba(255, 0, 0, 0.60);
}
.wrapMe{
    width: 100%;
    word-wrap: break-word;
}
.scroll{
    height: 27vh;
    overflow-y: scroll;
}
</style>
  