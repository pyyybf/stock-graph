<template>
  <div>
    <a-row style="top:200px">
      <a-col span="16" offset="4">
        <a-input-search
          :placeholder="this.ifInputId?'请输入股票ID':'请输入股票名称'"
          enter-button="查询"
          size="large"
          @search="onSearch"
        />
      </a-col>
      <br/><br/><br/>
      <a-col span="16" offset="4">
        查询方式：
        <a-radio-group name="radioGroup" :default-value="true" v-model="ifInputId">
          <a-radio :value="true">
            根据ID查询
          </a-radio>
          <a-radio :value="false">
            根据名称查询
          </a-radio>
        </a-radio-group>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  export default {
    name: 'Search',
    data() {
      return {
        ifInputId: true,
      }
    },
    methods: {
      onSearch(value) {
        if (value) {
          if (this.ifInputId && !isNaN(value)) {
            this.$router.push({
              name: 'StockDetail',
              params: {
                stockId: value
              }
            })
          } else {
            this.$router.push({
              name: 'StockDetail',
              params: {
                stockName: value
              }
            })
          }
        }
      }
    },
  }
</script>

<style scoped>

</style>
