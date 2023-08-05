import App from "./widget/App.vue";
import { createApp } from "vue";
import VueAxios from "vue-axios";
import axios from "axios";
import qs from "qs";
import i18n from "./widget/i18n.js";
import Base from "@patternslib/patternslib/src/core/base";

function axiosInstance() {
  const instance = axios.create({
    paramsSerializer: (params) =>
      qs.stringify(params, { arrayFormat: "repeat" }),
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      Prefer: "return=representation",
    },
  });
  return instance;
}

function initReferenceWidget(element) {
  if (element.classList.contains("initialized")) {
    return;
  }

  const app = createApp(App);
  app.use(VueAxios, {
    axios: axiosInstance(),
  });

  const messages = JSON.parse(element.getAttribute("data-translations"));
  app.use(i18n, messages);
  app.mount(element);
  element.classList.add("initialized");
}

window.initReferenceWidget = initReferenceWidget;

export default Base.extend({
  name: "reference-browser-widget",
  trigger: ".reference-widget-app",
  parser: "mockup",
  init() {
    initReferenceWidget(this.$el[0]);
  },
});
