import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import '@fortawesome/fontawesome-free/css/all.css'
Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        dark: true,
        themes: {
            dark: {
                primary: "#5D5C5C",
            },
        },
        icons: {
            iconfont: 'fa',
        },
    }
});