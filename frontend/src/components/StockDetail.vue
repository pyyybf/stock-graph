<template>
  <div class="">

    <div id="mount"></div>
    <a-row id="chart">
      <a-col :span="12">
        <div class="righttop" ref="charts1" style="height: 500px;width:500px"></div>
      </a-col>
      <a-col :span="12">
        <div class="righttop" ref="charts2" style="height: 500px;width:500px"></div>
      </a-col>
    </a-row>

  </div>



</template>

<script>
  import {getStockByIdAPI, getStockByNameAPI} from "../api";
  import G6 from '@antv/g6';
  import * as echarts from 'echarts';

  const colors = [
    '#BDEFDB',
    '#BDD2FD',
    '#F6C3B7',
  ];
  const strokes = [
    '#5AD8A6',
    '#5B8FF9',
    '#E8684A',
  ];

  export default {
    name: "StockDetail",
    data() {
      return {
        currentStockId: -1,
        currentStockName: '',
        pre_data: [5,3,23],
        avg_data: [1,1,1],
      }
    },
    async mounted() {
      if (this.$route.params.stockId) {
        this.currentStockId = this.$route.params.stockId;
        const res = await getStockByIdAPI(this.currentStockId);
        console.log(res.data.content) //包含stock，nodes，edges
        this.graphData = res.data.content;
        this.pre_data = [];
        this.pre_data[0] = res.data.content.stock.quarter_p;
        this.pre_data[1] = res.data.content.stock.halfYear_p;
        this.pre_data[2] = res.data.content.stock.year_p;
        this.avg_data = [];
        this.avg_data[0] = res.data.content.stock.quarter_a;
        this.avg_data[1] = res.data.content.stock.halfYear_a;
        this.avg_data[2] = res.data.content.stock.year_a;
      } else {
        this.currentStockName = this.$route.params.stockName;
        const res = await getStockByNameAPI(this.currentStockName);
        // console.log(res.data.content);
        this.graphData = res.data.content;
        this.graphData = res.data.content;
        this.pre_data = [];
        this.pre_data[0] = res.data.content.stock.quarter_p;
        this.pre_data[1] = res.data.content.stock.halfYear_p;
        this.pre_data[2] = res.data.content.stock.year_p;
        this.avg_data = [];
        this.avg_data[0] = res.data.content.stock.quarter_a;
        this.avg_data[1] = res.data.content.stock.halfYear_a;
        this.avg_data[2] = res.data.content.stock.year_a;


      }
      this.init();
      this.initbargraph1();
      this.initbargraph2();
    },
    methods: {
      init() {

        const mount = document.getElementById('mount');

        this.graphData.nodes.forEach((node) => {
          node.id = node.id.toString();
        });
        this.graphData.edges.forEach((edge) => {
          edge.source = edge.source.toString();
          edge.target = edge.target.toString();
        });

        this.graphData.nodes.forEach((node) => {
          node.style = {};
          if (node.cluster === '股票') {
            node.style.fill = colors[0];
            node.size = 60;
          } else if (node.cluster === '近期事件') node.style.fill = colors[1];
          else node.style.fill = colors[2];
        });

        const tooltip = new G6.Tooltip({
          offsetX: 10,
          offsetY: 10,
          itemTypes: ['node'],
          // 自定义 tooltip 内容
          getContent: (e) => {
            const outDiv = document.createElement('div');
            outDiv.style.width = 'fit-content';
            if(e.item.getModel().index === 0) outDiv.innerHTML = e.item.getModel().label;
            else outDiv.innerHTML = e.item.getModel().description.date;
            return outDiv;
          },
        });


        const graph = new G6.Graph({
          container: mount,
          center: true,
          width: 600,
          height: 500,
          plugins: [tooltip],
          modes: {
            default: [
              'zoom-canvas',
              'drag-canvas',
              'drag-node'
            ],
          },
          layout: {
            type: "force",
            nodeSpacing: 15,
            linkDistance: 100,
            preventOverlap: true,
          },
          defaultNode: {
            type: 'circle',
            size: 40,
            labelCfg: {
              style: {
                fontSize: 10
              }
            }
          },
        });
        // console.log(this.graphData);
        graph.data(this.graphData);
        graph.render();


        graph.on('node:dragstart', function (e) {
          graph.layout();
          refreshDragedNodePosition(e);
        });
        graph.on('node:drag', function (e) {
          refreshDragedNodePosition(e);
        });
        graph.on('node:dragend', function (e) {
          e.item.get('model').fx = null;
          e.item.get('model').fy = null;
        });

        function refreshDragedNodePosition(e) {
          const model = e.item.get('model');
          model.fx = e.x;
          model.fy = e.y;
        }

        this.graphData.nodes.forEach(function (node) {
          node.oriSize = node.size;
          node.oriLabel = node.label;
        });

        graph.on('node:click', function (e) {
          const node = e.item;
          const states = node.getStates();
          let clicked = false;
          const model = node.getModel();
          let size = 100;
          let labelText = model.oriLabel + '\n Date: ' + model.description.date + '\n';
          if (model.description.conductor !== '--') {
            labelText += 'Conductor: ' + model.description.conductor + '\n';
          }
          if (model.description.amount !== '--') {
            labelText += 'Amount: ' + model.description.amount + '\n';
          }
          states.forEach(function (state) {
            if (state === 'click') {
              clicked = true;
              size = model.oriSize;
              labelText = model.oriLabel;
            }
          });
          graph.setItemState(node, 'click', !clicked);
          graph.updateItem(node, {
            size,
            label: labelText,
          });
          graph.layout();
        });

      },


      initbargraph1() {
        let myChart = echarts.init(this.$refs.charts1, "macarons");
        myChart.setOption({
          title: {
            text: '历史持有盈利概率',
            // subtext:'图例表示了在此知识图谱中，关系的类型与关系类型的分布情况'
          },
          grid: {
            top: 90
          },
          tooltip: {},
          xAxis: {
            data: ['季度','半年','一年']
          },
          yAxis: {},
          series: [{
            name: '数量',
            type: 'bar',
            data: this.pre_data,
            barWidth: '50%'
          }]
        })
      },
      initbargraph2() {
        let myChart = echarts.init(this.$refs.charts2, "macarons");
        myChart.setOption({
          title: {
            text: '平均持有盈利概率',
            // subtext:'图例表示了在此知识图谱中，关系的类型与关系类型的分布情况'
          },
          grid: {
            top: 90
          },
          tooltip: {},
          xAxis: {
            data: ['季度','半年','一年']
          },
          yAxis: {},
          series: [{
            name: '数量',
            type: 'bar',
            data: this.avg_data,
            barWidth: '50%'
          }]
        })
      },
    },
  }
</script>

<style scoped>
  #mount {
    background-color: aliceblue;
  }
  #chart {
    background-color: aliceblue;
  }
  .g6-component-tooltip {
    background-color: rgba(255, 255, 255, 0.8);
    padding: 0px 10px 24px 10px;
    box-shadow: rgb(174, 174, 174) 0px 0px 10px;
  }
  .righttop{
    width: 100%;
    height: 100%;
  }
</style>
