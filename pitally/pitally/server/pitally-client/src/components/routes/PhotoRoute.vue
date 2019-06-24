<template>
  <div class>
    <div class="preview fixed absolute--fill bg-light-gray w-50">
      <div class="absolute right-0 ma3 z-5">
<!-- TODO warning messaged, add a class+some css or something -->
        <p :hidden="$store.deviceInfo.status!='unreachable'"> This device appears unreachable. 
          If this problem persist, try rebooting it or fixing its connection.</p>

        <p :hidden="$store.deviceInfo.status!='recording'"> This device is curently recording a video. 
          You need to <a href="/#/video">stop the video</a> before taking any still picture.</p>
        <v-btn
          :disabled="$store.isPreviewing || $store.deviceInfo.status != 'idle'"
          :loading="$store.loadings.isCapturingImg"
          type="submit"
          color="primary"
          @click="$store.captureImage"
        >
          <v-icon left>photo_camera</v-icon>Capture
        </v-btn>
        <div>
          <v-switch 
          :disabled="$store.loadings.isCapturingImg  || $store.deviceInfo.status != 'idle'"
          v-model="$store.isPreviewing" label="Preview"></v-switch>
        </div>
      </div>
      <img v-show="$store.isPreviewing" v-if="$store.previewImg" :src="$store.previewImg.image" alt>
      <img v-show="!$store.isPreviewing" :src="$store.images.length && $store.images[0].image" alt>
         <pre v-if='$store.$data.devMode != "production"' class="absolute z-2 top-0">{{ $store.$data }}</pre>
    </div>

    <div class="settings bg-white relative z-1 shadow-1">
      <v-tabs color="primary" dark>
        <v-tab>Images</v-tab>
        <v-tab>Settings</v-tab>
        <v-tab-item>
          <div class="pa4">
            <!-- <div>
              <button type="button">Download</button>
              <button type="button">Delete</button>
            </div>-->
            <p v-if="!$store.images.length">You don't have any image for now</p>
            <div v-else>
              <v-btn @click="removeImages">Delete</v-btn>
              <v-btn>Download</v-btn>
              <ImagesTable/>
            </div>
          </div>
        </v-tab-item>
        <v-tab-item>
          <div class="pa4">
            <CameraSettingsForm/>
          </div>
        </v-tab-item>
      </v-tabs>
    </div>
  </div>
</template>

<script>
import CameraSettingsForm from '../CameraSettingsForm'
import ImagesTable from '../ImagesTable'
export default {
  name: 'PhotoRoute',
  components: {
    CameraSettingsForm,
    ImagesTable,
  },
  data: () => ({

  }),
  methods: {
    removeImages() {
      this.$store.removeImages(this.$store.selectedImgs)
    }
  }
}
</script>
<style scoped>
.settings {
  margin-left: 50%;
  min-height: 100vh;
}
</style>
