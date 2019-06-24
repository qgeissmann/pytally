<template>
  <v-data-table
    v-model="$store.deviceList"
    :headers="headers"
    :items="$store.deviceList"
    :pagination="pagination"
    item-key="hostname"
    select-all
  >
    <template slot="items" slot-scope="props">
      <td>
        <v-checkbox v-model="props.item.selected" primary hide-details></v-checkbox>
      </td>
      <td>
        <a :href="'http://' + props.item.hostname + '.lan'"  width="33">{{ props.item.hostname }} </a>
        </td>
      <td>
        <a :href="'http://' + props.item.hostname + '.lan' + '/#/photo'"  width="33"><v-icon left>photo_camera</v-icon> </a>
        <a :href="'http://' + props.item.hostname + '.lan' + '/#/video'" width="33"><v-icon left>videocam</v-icon> </a>
      </td>

      <td>{{ props.item.status }}</td>
      <td>{{ props.item.software_version }}</td>
      <td>{{ props.item.percent_disk_use}}</td>
      <td>{{ props.item.ip }}</td>
      <td>{{ props.item.mac }}</td>
    </template>

  </v-data-table>
</template>
<script>
export default {  
  name: 'DeviceTable',
  data: () => ({
    headers: [
      { text: 'Name', value: 'hostname'},
      { text: 'Action', value: 'hostname'},
      { text: 'Status', value: 'status'},
      { text: 'Software version', value: 'software_version'},
      { text: 'Used disk space (%)', value: 'percent_disk_use'},
      { text: 'IP address', value: 'ip'},
      { text: 'MAC', value: 'mac' },
    ],
  pagination:{
    descending: true,
    page: 1,
    rowsPerPage: -1,
    sortBy: "hostname",
    totalItems: null
    }
  }),
}
</script>
<style scoped>
</style>

