<template>
  <form @submit.prevent="onSubmit" novalidate role="form" class="form">
    <div class="fields">
      <v-text-field
        label="Prefix"
        placeholder="Type a prefix"
        type="text"
        :disabled="$store.isPreviewing"
        v-model="$store.settings.prefix"
        name="prefix"
      />
      <v-select
        label="Resolution"
        name="resolution"
        :disabled="$store.isPreviewing"
        :items="$store.availableResolutions"
        v-model="$store.currentResolution"
      ></v-select>
      <v-text-field
        label="ISO"
        placeholder="Type a number"
        type="number"
        name="iso"
        min="100"
        max="800"
        step="100"
        v-model="$store.settings.iso"
      />
      <v-text-field
        label="Shutter speed"
        placeholder="Type a number"
        type="number"
        name="shutter_speed"
        min="1000"
        max="10000000"
        step="100"
        v-model="$store.settings.shutter_speed"
      />

      <v-text-field
        label="Red gain"
        placeholder="Type a number"
        type="number"
        step="0.05"
        min="0.0"
        max="8.0"
        name="awb_gain_r"
        v-model="$store.settings.awb_gain_r"
      />
      <v-text-field
        label="Blue gain"
        placeholder="Type a number"
        type="number"
        step="0.05"
        min="0.0"
        max="8.0"
        name="awb_gain_b"
        v-model="$store.settings.awb_gain_b"
      />
    </div>
  </form>
</template>
<script>
export default {
  name: 'CameraSettingsForm',
  methods: {
    onSubmit() {
      this.$store.captureImage()
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

