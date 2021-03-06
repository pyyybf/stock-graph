import Vue from 'vue'
import Router from 'vue-router'
import Search from '@/components/Search'
import StockDetail from '@/components/StockDetail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Search',
      component: Search
    },
    {
      path: '/stockDetail/:stockId?/:stockName?',
      name: 'StockDetail',
      component: StockDetail,
    }
  ]
})
