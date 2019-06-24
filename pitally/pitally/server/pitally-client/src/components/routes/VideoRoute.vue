<template>
  <div class>
    <div class="preview fixed absolute--fill bg-light-gray w-50">
      <div class="absolute right-0 ma3 z-5">
        <v-btn
          :disabled="$store.deviceInfo.status!='idle'"  
          :loading="$store.loadings.isStartingVideo || $store.loadings.isStoppingVideo"
          type="submit"
          color="primary"
          @click="$store.startVideo"
        >
          <v-icon left>videocam</v-icon>Start Video
        </v-btn>
        
        <v-btn
          :disabled="$store.deviceInfo.status != 'recording'"
          :loading="$store.loadings.isStartingVideo || $store.loadings.isStoppingVideo"
          type="submit"
          color="primary"
          @click="$store.stopVideo"
        >
          <v-icon left>stop</v-icon>Stop Video
        </v-btn>
      <p v-if="$store.videoPreviewImg"> {{ $store.videoPreviewImg.videoBasename }} </p>
      
      </div>
      <img v-show="$store.deviceInfo.status === 'recording'" :src="$store.videoPreviewImg && $store.videoPreviewImg.image" alt>
         <pre v-if='$store.$data.devMode != "production"' class="absolute z-2 top-0">{{ $store.$data }}</pre>
    </div>

    <div class="settings bg-white relative z-1 shadow-1">
      <v-tabs color="primary" dark>
        <v-tab>Settings</v-tab>
        <v-tab-item>
          <div class="pa4">
            <VideoSettingsForm/>
          </div>
        </v-tab-item>
      
        <v-tab>Video Info</v-tab>
      
        <v-tab-item>
          <div class="pa4">
            <!-- <div>
              <button type="button">Download</button>
              <button type="button">Delete</button>
            </div>-->
            <!-- <p v-if="!$store.images.length">You don't have any image for now</p> -->
            <!-- <div v-else> -->
              <!-- <v-btn @click="removeImages">Delete</v-btn> -->
              <!-- <v-btn>Download</v-btn> -->
              <!-- <ImagesTable/> -->
            <!-- </div> -->
          </div>
        </v-tab-item>
        </v-tabs>
    </div>
  </div>
</template>


<script>
import VideoSettingsForm from '../VideoSettingsForm'
export default {
  name: 'VideoRoute',
  components: {
    VideoSettingsForm,
  },
  data: () => ({

  }),

}
</script>
<style scoped>
.settings {
  margin-left: 50%;
  min-height: 100vh;
}
</style>
