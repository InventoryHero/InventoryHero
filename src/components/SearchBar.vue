<template>
    <div id="containerSearchBar">
        <input :class="this.do_transform" type="text" v-model="this.value" @input="this.$emit('valueUpdated', this.value)">
        <i class="fa-solid fa-magnifying-glass fa-lg icon"></i>
    </div>
</template>

<script>


export default {
    name: 'searchBar',
    data() {
          return {
              value: ""
          }
      },
    props: {
        do_transform: {
            type: String,
            default: "transform",
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#containerSearchBar{ 
    position: relative;
    width: 80%;
    height: 50px;
    border: white solid 2px;
    margin-left: 50%;
    margin-bottom: 80px;
    transform: translateX(-50%);
    top: 50px;
    border-radius: 25px;
}
.transform{
    transform: translateX(-50%);
}
.icon {
    position: absolute;
    left: 20px;
    top: 21px;
    transform: translateY(-50%);
}

input {
    position: absolute;
    width: 100%;
    height: 100%;

    border-radius: 25px;
    padding-left: 50px;
    color: white;
}

input:focus{
    outline: none;
    border-color: inherit;
    -webkit-box-shadow: none;
    box-shadow: none;
}

</style>
  