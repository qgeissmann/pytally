import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import Vue from "vue";
import App from "./App.vue";
import router from "./routes";
import store from "./store";
import FormItem from "./components/ui/FormItem";
import "vuetify/dist/vuetify.min.css"; // Ensure you are using css-loader
import Vuetify from "vuetify";
Vue.use(Vuetify, {
  theme: {
    primary: "#e91e63",
    secondary: "#3f51b5",
    accent: "#f44336",
    error: "#ffeb3b",
    warning: "#00bcd4",
    info: "#03a9f4",
    success: "#4caf50"
  }
});

Vue.config.productionTip = false;
Vue.component("FormItem", FormItem);

Vue.use(_Vue => {
  _Vue.prototype.$store = store;
});

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
