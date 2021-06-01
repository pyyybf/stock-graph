// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import {Col, Descriptions, Input, Radio, Row, Table, Timeline, Icon} from 'ant-design-vue'

Vue.config.productionTip = false;

Vue.use(Input);
Vue.use(Row);
Vue.use(Col);
Vue.use(Radio);
// Vue.use(Descriptions);
// Vue.use(Table);
// Vue.use(Timeline);
// Vue.use(Icon);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
})
