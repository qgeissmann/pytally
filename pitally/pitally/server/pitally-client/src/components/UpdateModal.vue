<!-- template for the modal component -->
<template>
<modal>
<h3 slot="header">Update selected devices</h3>
<div slot="body">
  <div v-if=" nNonIdle != 0">
    <p> The selection contains devices that are not idle ({{ nNonIdle }}). 
        Only idle ones can be updated </p>
  </div>
  
  <div v-else>
    <label>File
      <input type="file" id="updateFile" ref="updateFile" v-on:change="handleUpdateFileUpload()"/>
    </label>
  </div>
</div>

<div slot="footer">
  <div v-if=" nNonIdle != 0  | this.$store.selectedDevices.length < 1">
    <button class="modal-default-button" @click="$store.$data.modal = null"> 
        Cancel
    </button>
  </div>
   <div v-else>
    <button class="modal-default-button" @click="$store.$data.modal = null"> 
        Cancel
    </button>
<!-- todo disable if uploadfile ==='' -->
    <button class="modal-default-button" @click="$store.uploadUpdateFile"> 
        Update {{this.$store.selectedDevices.length }} device(s)
    </button>
  </div>
  
</div>
</modal>
</template>

<script>
import Modal from './ui/Modal'

export default {
  name: 'UpdateModal',
  components: {
    Modal
  },
  methods:{
    handleUpdateFileUpload(){
      this.$store.updateUpdateFile(this.$refs.updateFile.files[0])
    }
  },
  computed:{
     nNonIdle() {
       var out = 0;
       for (const i in this.$store.selectedDevices){
         console.log(this.$store.selectedDevices[i].status);
         if(this.$store.selectedDevices[i].status != 'idle'){
            out = out + 1;
         }
       }
      return out;
    }
  }
}

</script>
<style scoped>
</style>

