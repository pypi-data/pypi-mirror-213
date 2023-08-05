export default {
  install: (app, options) => {
    app.config.globalProperties.$i18n = (message) => {
      if (message in options) {
        return options[message];
      }
      return message;
    };
  },
};
