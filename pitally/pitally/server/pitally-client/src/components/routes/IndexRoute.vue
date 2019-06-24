<template>
  <div class>
   <div class="pa4">
    <div class="absolute right-1 ">
  <v-btn
        type="submit"
        color="primary"
        @click="$store.listDevices"
      >
        <v-icon left>refresh</v-icon>Find devices
      </v-btn>
    </div>
  <DeviceTable/>
  <div class="absolute right-1 ">
      <v-btn
          type="submit"
          color="primary"
          @click="$store.listDevices"
        >
          <v-icon left>refresh</v-icon>Update

        </v-btn>
        <button id="show-modal" @click="$store.$data.modal = 'update'">Show Modal</button>
        <!-- use the modal component, pass in the prop -->
          <UpdateModal v-if="$store.$data.modal === 'update'" @close="$store.$data.modal = null"/>
  </div>

  </div>
   <pre v-if='$store.$data.devMode != "production"' class="z-2 top-0">{{ $store.$data }}</pre>
 
   </div>

</template>

<script>
import DeviceTable from '../DeviceTable'
import UpdateModal from '../UpdateModal'

export default {
  name: 'IndexRoute',
  components: {
    DeviceTable,
    UpdateModal
  },
  data: () => ({

  }),
}
</script>
<style scoped>
</style>
