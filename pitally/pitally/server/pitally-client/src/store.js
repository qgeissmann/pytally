import axios from "axios";
import dayjs from "dayjs";
import Vue from "vue";

const httpClient = axios.create({
  baseURL: process.env.NODE_ENV === "development" ? "http://localhost:5000" : "/"
});

export default new Vue({
  data: () => ({
    devMode: process.env.NODE_ENV,
    settings: {
      iso: 200,
      resolution: "640x480",
      shutter_speed: 10000,
      awb_gain_r: 1,
      awb_gain_b: 1,
      prefix: "my-image"
    },
    videoSettings: {
      prefix: "my-video",
      resolution: "1640x1232",
      bitrate: 2500000,
      fps:25,
      duration:-1,
      start_time:"",
      clip_duration:300,
      end_of_clip_hw_class_name: "None"
    },
    previewImg: null,
    videoPreviewImg: null, 
    images: [],
    loadings: {
      isCapturingImg: false,
      isStartingVideo: false,
      isStoppingVideo: false,
      isMakingVideoLib: false,
      isUpdating: false
    },
    selectedImgs: [],
    availableVideoResolutions: ["640x480", "1640x1232"],
    availableResolutions: ["640x480", "1640x1232", "3280x2464"],
    availableHWController: ["None", "y-roulette"], // todo, retreive this from the server!
    previewResolution: "640x480",
    isPreviewing: false,
    deviceList: [],
    deviceInfo: {}, // device_info = device_info = {"id": MACHINE_ID, "status": "idle", "since": time.time()}
    modal: null, // "upload", "video_start","",
    updateFile: '',
    videoLibrary: []
  }),
  created () {
    this.listDevices();
    this.updateDeviceInfo();
    //setInterval(this.updateDeviceInfo, 1000);
    setInterval(this.updateAllDevicesInfo, 3000);
    setInterval(this.listDevices, 30000);
    setInterval(this.previewVideo, 1000);
  },
  destroyed () {
    //clearInterval(this.updateDeviceInfo);
    clearInterval(this.listDevices);
    clearInterval(this.updateAllDevicesInfo);
    clearInterval(this.previewVideo);
  },

  methods: {
    async makeVideoLibrary(){
      try{
        this.loadings.isMakingVideoLib = true
        var resp = []
        try{
          const response = await httpClient.get("/list_video_on_ftp");
          resp = response.data;
          }
        catch(e){
          resp = []
        }
        var lib = []
        for(const i in resp){
          var r = resp[i]
          r["format"] = r.w + "x" + r.h + "@" + r.fps
          r["link"] = "ftp://pitally-drive/" + r.path
          lib.push(r)
        }
        this.videoLibrary = lib}
      finally{
        this.loadings.isMakingVideoLib = false
      }
    },
    async updateDeviceInfo() {

      try{
        const response = await httpClient.get("/device_info");
        this.deviceInfo = response.data;
        }
      catch(e){
        this.deviceInfo.status="unreachable"
      }
    },

    async updateAllDevicesInfo(list = null) {

      var out = []
      if(list === null){
        for(const i in this.deviceList){
          out.push(this.deviceList[i])
        }
      }
      else{
        out = list
      }
      if(process.env.NODE_ENV != "development" & !process.env.VUE_APP_MOCK ){

        for(const i in out){
          const url = out[i].url + "/device_info"
          if(out[i].hostname === "pitally-drive"){
            continue
          } 
          
          if(url){
            axios.get(url).then((response) => {
            for(const k in response.data){
              out[i][k] = response.data[k]; 
              }}
              )
            }          
          }
        }
        else{
          for(const i in out){
            const url = out[i].url + "/device_info"
            if(url){
                out[i].software_version= Math.random()
              }          
            }
        }
        // force update of device list
        if(list === null){
          this.forceDevListUpdate() 
        }
    },
    
    forceDevListUpdate(){
      var  swap = []
        for(const i in this.deviceList){
          swap.push(this.deviceList[i])
        }
        this.deviceList = swap
    },

    async listDevices() {
      if(process.env.VUE_APP_MOCK === "True"){
        console.log(process.env.VUE_APP_MOCK)
        this.deviceList  = [
          { hostname: 'pitally-uvwxyz', url: 'http://pitally-uvwxyz.lan' , status: 'idle', ip: '1.2.3.4', selected:false},
          { hostname: 'pitally-fghijk', url: 'http://pitally-fghijk.lan', status: 'idle', ip: '1.2.3.5', selected:false},
          { hostname: 'pitally-klmnop', url: 'http://pitally-klmnop.lan', status: 'recording', ip:'1.2.3.4', selected:false},
        ]
      }
      else{
        const r = httpClient.get("/list_devices").then(
        response => {
          var list_dev = response.data;
          this.updateAllDevicesInfo(list_dev)
          for(const i in list_dev){
            var hn = list_dev[i].hostname
            for(const j in this.deviceList){
              if(hn == this.deviceList[j].hostname){
                console.log(hn + this.deviceList[j].selected)
                if(this.deviceList[j].selected != null){
                  list_dev[i].selected = this.deviceList[j].selected
                }
                else{
                  list_dev[i].selected = false
                }
              }
            }
          }
          this.deviceList = list_dev;
          
        });
      }
    },
    async startVideo(e, _settings) {
      const settings = _settings || this.postVideoData;
      console.log(this.postVideoData);
      
      settings['time'] = Date.now();
      
      try{
        this.loadings.isStartingVideo = true;
        await httpClient.post("/start_video", settings).then(
          response => {
            this.deviceInfo = response.data;         
          }
        )
      }
      finally{
        this.loadings.isStartingVideo = false;
      }
    },
    async stopVideo() {
      try{
        this.loadings.isStoppingVideo = true;
        await httpClient.post("/stop_video", {}).then(
          response => {
            this.deviceInfo = response.data;         
          }
        )
      }
      finally{
        this.loadings.isStoppingVideo = false;
      }
    },
    async previewVideo() {
      if(this.deviceInfo.status != "recording"){
        return null;
      }
        
      await httpClient.post("/video_preview").then(
        response => {
          const newImage = {
            "image": response.data.image,
            "videoBasename": response.data.video_name,
          };
          console.log(newImage);
          this.videoPreviewImg = newImage;
          
        }
      )
    },
    async captureImage(e, _settings) {
      const settings = _settings || this.postCaptureData;
      const timestamp = dayjs().toJSON();
      this.loadings.isCapturingImg = true;

      try {
        const { prefix, image } = await httpClient.post("/capture/1", settings);
        const newImage = {
          timestamp,
          filename: `${prefix}_${timestamp}.jpg`,
          image,
          selected: true
        };
        this.images.unshift(newImage);
        return newImage;
      } finally {
        this.loadings.isCapturingImg = false;
      }
    },
    async previewImage(_settings) {
      const settings = _settings || this.postCaptureData;
      const timestamp = dayjs().toJSON();
      await httpClient.post("/capture/1", settings).then(
        response => {
          const newImage = {
            "image": response.data.image,
            "timestamp": timestamp,
          };
          console.log(newImage);
          this.previewImg = newImage;
          
        }
      )
    },
    removeImages(imgs) {
      for (const img of imgs) {
        const index = this.images.findIndex(_img => _img === img);
        Vue.delete(this.images, index);
      }
      this.selectedImgs = [];
    },
    updateUpdateFile(file){
      this.updateFile =  file;
    },
    uploadUpdateFile(e_, port=8080, route="/"){
      console.log(this.updateFile)
      let formData = new FormData();
      formData.append('package_file', this.updateFile);
      var report = {}
      var promises = []
      var devs = this.selectedDevices;
      try{
        
          //clearInterval(this.updateAllDevicesInfo);
          for(const i in devs){
            report[devs[i].hostname] = "processing"
            const url = devs[i].url
            const finalUrl = url + ":" + port + route
            console.log(finalUrl)
            const p = axios.post( finalUrl,
                        formData,
                        {
                          headers: {
                              'Content-Type': 'multipart/form-data'
                          }
                        }).then(function(){
                          report[devs[i].hostname] = "success"
                          console.log(report);
                        }).catch(function(){
                          report[devs[i].hostname] = "failure"
                          console.log(finalUrl)
                          console.log(report);
                        })
            promises.push(p)
            }
            axios.all(promises).then(function(){
                console.log("all finished");
                console.log(report);
                
              });
            

      }
      finally{
        //  this.modal="null"
        this.updateFile = ""
      }
    }

  },
  watch: {
    isPreviewing(val) {
      const previewRecursive = async () => {
        await this.previewImage();
        if (this.isPreviewing) previewRecursive();
      };
      if (val) {
        previewRecursive();
      }
    }
  },
  computed: {
    selectedDevices:{
      get(){
        const out = [];
        for(const i in this.deviceList){
          if(this.deviceList[i].selected)
          out.push(this.deviceList[i]);    
        }
        return out;
    }
    },
    postVideoData: { 
      get () {
        const res = this.videoSettings.resolution.split("x");
        const out = this.videoSettings;
        out['w'] = res[0];
        out['h'] = res[1];
        return(out)
      }
    } ,
    postCaptureData: { 
      get () {
        const res = this.settings.resolution.split("x");
        const out = this.settings;
        out['w'] = res[0];
        out['h'] = res[1];
        return(out)
      }
    } ,
    currentResolution: {
      get() {
        return this.isPreviewing
          ? this.previewResolution
          : this.settings.resolution;
      },
      set(val) {
        this.settings.resolution = val;
      }
    }
  }
});

// // DeV test
// if (process.env.VUE_APP_MOCK) {
//   const createResp = () =>
//     new Promise(resolve => {
//       setTimeout(
//         () =>
//           resolve({
//             image:
//               "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAIAAADTED8xAAADMElEQVR4nOzVwQnAIBQFQYXff81RUkQCOyDj1YOPnbXWPmeTRef+/3O/OyBjzh3CD95BfqICMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMO0TAAD//2Anhf4QtqobAAAAAElFTkSuQmCC",
//             prefix: ""
//           }),
//         1000
//       );
//     });
//   httpClient.interceptors.response.use(
//     function(response) {
//       // Do something with response data
//       return createResp();
//     },
//     function(error) {
//       // Do something with response error
//       return createResp();
//     }
//   );
// }
