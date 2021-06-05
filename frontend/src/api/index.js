import HttpRequest from '@/axios/api.request'

const api = {
  stockPre: '/api/stock',
  eventPre: '/api/event',
}

export const getStockByIdAPI = (parameter) => {
  return HttpRequest.request({
    url: `${api.stockPre}/getStockById`,
    method: 'get',
    params: {id: parameter}
  })
}

export const getStockByNameAPI = (parameter) => {
  return HttpRequest.request({
    url: `${api.stockPre}/getStockByName`,
    method: 'get',
    params: {name: parameter}
  })
}

export const ifExistAPI = (parameter) => {
  return HttpRequest.request({
    url: `${api.stockPre}/ifExist`,
    method: 'get',
    params: {
      id: parameter.id,
      name: parameter.name
    }
  })
}
