<template>
  <form 
          :disabled="$store.deviceInfo.status!='idle'"
          @submit.prevent="onSubmit" novalidate role="form" class="form">
    <div class="fields">
      <v-text-field
        label="Prefix"
        placeholder="Type a prefix"
        type="text"
        :disabled="$store.isPreviewing"
        v-model="$store.videoSettings.prefix"
        name="prefix"
      />
      <v-select
        label="Resolution (px)"
        name="resolution"
        :disabled="$store.isPreviewing"
        :items="$store.availableVideoResolutions"
        v-model="$store.videoSettings.resolution"
      ></v-select>
      <v-text-field
        label="FPS (1/s)"
        placeholder="Type a number"
        type="number"
        name="fps"
        min="1"
        max="30"
        step="1"
        v-model="$store.videoSettings.fps"
      />
      <v-text-field
        label="Bitrate (bps)"
        placeholder="Type a number"
        type="number"
        name="bitrate"
        min="1000000"
        max="25000000"
        step="1000"
        v-model="$store.videoSettings.bitrate"
      />

      <v-text-field
        label="Video duration (h)"
        placeholder="Type a number"
        type="number"
        step="2"
        min="0.0"
        name="duration"
        v-model="$store.videoSettings.duration"
      />

      <v-text-field
        label="Start time"
        placeholder="YYYY-MM-DD hh:mm:ss"
        type="text"
        :disabled="$store.isPreviewing"
        v-model="$store.videoSettings.start_time"
        name="start_time"
      />
      
      <v-text-field
        label="Clip duration (s)"
        placeholder="Type a number"
        type="number"
        name="clip_duration"
        min="60"
        max="86400"
        step="60"
        v-model="$store.videoSettings.clip_duration"
      />

      <v-select
        label="Hardware controller"
        name="end_of_clip_hw_class_name"
        :disabled="$store.isPreviewing"
        :items="$store.availableHWController"
        v-model="$store.videoSettings.end_of_clip_hw_class_name"
      ></v-select>

    </div>
  </form>
</template>
<script>
export default {
  name: 'VideoSettingsForm',
  methods: {
    onSubmit() {
      this.$store.recordVideo()
    }
  }
}
</script>
<style scoped>
.fields {
  display: grid;
  grid-gap: 0.5rem;
}
</style>

