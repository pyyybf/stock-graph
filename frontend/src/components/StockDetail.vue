<template>
  <div class="stock-detail">
    <a-descriptions title="股票信息" :column="6" bordered>
      <a-descriptions-item label="股票ID" :span="2">
        {{this.currentStockInfo.id}}
      </a-descriptions-item>
      <a-descriptions-item label="名称" :span="2">
        {{this.currentStockInfo.name}}
      </a-descriptions-item>
      <a-descriptions-item label="总担保金额（人民币）" :span="2">
        {{this.currentStockInfo.guarantee_a}}亿元
      </a-descriptions-item>
      <a-descriptions-item label="季度盈利概率" :span="3">
        {{this.currentStockInfo.quarter_p}}
      </a-descriptions-item>
      <a-descriptions-item label="季度盈利额" :span="3">
        {{this.currentStockInfo.quarter_a}}
      </a-descriptions-item>
      <a-descriptions-item label="半年盈利概率" :span="3">
        {{this.currentStockInfo.halfYear_p}}
      </a-descriptions-item>
      <a-descriptions-item label="半年盈利额" :span="3">
        {{this.currentStockInfo.halfYear_a}}
      </a-descriptions-item>
      <a-descriptions-item label="全年盈利概率" :span="3">
        {{this.currentStockInfo.year_p}}
      </a-descriptions-item>
      <a-descriptions-item label="全年盈利额" :span="3">
        {{this.currentStockInfo.year_a}}
      </a-descriptions-item>
      <a-descriptions-item label="事件" :span="6">
          <span v-for="event in this.currentEventList">
            {{event.date.split('-')[0]}}年{{event.date.split('-')[1]}}月{{event.date.split('-')[2]}}日 {{event.type}}<br/>
          </span>
      </a-descriptions-item>
    </a-descriptions>
  </div>
</template>

<script>
  import {getStockByIdAPI, getStockByNameAPI} from "../api";

  export default {
    name: "StockDetail",
    data() {
      return {
        currentStockId: -1,
        currentStockName: '',
      }
    },
    async mounted() {
      if (this.$route.params.stockId) {
        this.currentStockId = this.$route.params.stockId;
        const res = await getStockByIdAPI(this.currentStockId);
        console.log(res.data.content) //包含stock，nodes，edges
      } else {
        this.currentStockName = this.$route.params.stockName;
        const res = await getStockByNameAPI(this.currentStockName);
        console.log(res.data.content)
      }
    },
    methods: {

    },
  }
</script>

<style scoped>
  .stock-detail {
    padding: 80px;
  }
</style>
