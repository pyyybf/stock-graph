<template>
  <div id="all">
    <div id="bar">
      <div class="headerContent">股票名称：{{currentStockName}}</div>
      <div class="headerContent">股票ID：{{(Array(6).join(0) + parseInt(currentStockId)).slice(-6)}}</div>
      <div class="headerContent"> 总担保额：￥{{guarantee_a.toFixed(2)}}（亿元）</div>

    </div>
    <a-divider></a-divider>

    <div id="details">
      <a-row>
        <a-col :span="15">
          <a-row class="graph" type="flex" justify="space-around" align="middle">
            <a-col :span="12" id="text2">近期事件与处罚事件</a-col>
            <a-col :span="12">
              <span class="pin"><img src="../assets/circle.png"/>  股票  </span>
              <span class="pin"><img src="../assets/circle2.png"/>   处罚事件  </span>
              <span class="pin"><img src="../assets/circle3.png"/>   近期事件  </span>
            </a-col>
          </a-row>
          <!--挂载G6图谱-->
          <div id="mount"></div>
        </a-col>
        <a-col :span="8" :offset="1" id="chart">
          <div class="righttop" ref="charts1" style="width: 100%;height: 300px"></div>
          <div class="righttop" ref="charts2" style="width: 100%;height: 300px"></div>
        </a-col>
      </a-row>

    </div>
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

  export default {
    name: "StockDetail",
    data() {
      return {
        currentStockId: -1,
        currentStockName: '',
        graphData: {},
        pre_data: [],
        avg_data: [],
        pre_data_col: [],
        avg_data_col: [],
        guarantee_a: 0,
      }
    },
    async mounted() {
      //按照stockId查询
      if (this.$route.params.stockId) {
        this.currentStockId = this.$route.params.stockId;
        const res = await getStockByIdAPI(this.currentStockId);
        // 获得图谱数据
        this.graphData = res.data.content;
        this.pre_data = [];
        this.pre_data_col = [];
        if (res.data.content.stock.quarter_p > -2) {
          this.pre_data.push(res.data.content.stock.quarter_p)
          this.pre_data_col.push('季度')
        }
        if (res.data.content.stock.halfYear_p > -2) {
          this.pre_data.push(res.data.content.stock.halfYear_p)
          this.pre_data_col.push('半年')
        }
        if (res.data.content.stock.year_p > -2) {
          this.pre_data.push(res.data.content.stock.year_p)
          this.pre_data_col.push('一年')
        }
        this.avg_data = [];
        this.avg_data_col = [];
        if (res.data.content.stock.quarter_a > -2) {
          this.avg_data.push(res.data.content.stock.quarter_a)
          this.avg_data_col.push('季度')
        }
        if (res.data.content.stock.halfYear_a > -2) {
          this.avg_data.push(res.data.content.stock.halfYear_a)
          this.avg_data_col.push('半年')
        }
        if (res.data.content.stock.year_a > -2) {
          this.avg_data.push(res.data.content.stock.year_a)
          this.avg_data_col.push('一年')
        }
        this.guarantee_a = res.data.content.stock.guarantee_a;
        this.currentStockName = res.data.content.stock.name;
      }
      // 按照股票名称查询
      else {
        this.currentStockName = this.$route.params.stockName;
        const res = await getStockByNameAPI(this.currentStockName);
        // 获得图谱数据
        this.graphData = res.data.content;
        this.pre_data = [];
        this.pre_data[0] = res.data.content.stock.quarter_p;
        this.pre_data[1] = res.data.content.stock.halfYear_p;
        this.pre_data[2] = res.data.content.stock.year_p;
        this.avg_data = [];
        this.avg_data[0] = res.data.content.stock.quarter_a;
        this.avg_data[1] = res.data.content.stock.halfYear_a;
        this.avg_data[2] = res.data.content.stock.year_a;
        this.guarantee_a = res.data.content.stock.guarantee_a;
        this.currentStockId = res.data.content.stock.id;
      }
      this.initG6();
      this.initbargraph1();
      this.initbargraph2();
    },
    methods: {
      initG6() {
        //挂载G6的element
        const mount = document.getElementById('mount');
        // 将int格式的id, source, target转为string
        this.graphData.nodes.forEach((node) => {
          node.id = node.id.toString();
        });
        this.graphData.edges.forEach((edge) => {
          edge.source = edge.source.toString();
          edge.target = edge.target.toString();
        });
        // 根据三种类型（股票、近期事件、惩罚事件）分配颜色
        this.graphData.nodes.forEach((node) => {
          node.style = {};
          if (node.cluster === '股票') {
            node.style.fill = colors[0];
            node.size = 60;
          } else if (node.cluster === '近期事件') node.style.fill = colors[1];
          else node.style.fill = colors[2];
        });
        // 鼠标悬浮窗，显示日期
        const tooltip = new G6.Tooltip({
          offsetX: 10,
          offsetY: 10,
          itemTypes: ['node'],
          getContent: (e) => {
            const outDiv = document.createElement('div');
            outDiv.style.width = 'fit-content';
            if (e.item.getModel().index === 0) outDiv.innerHTML = e.item.getModel().label;
            else outDiv.innerHTML = e.item.getModel().description.date;
            return outDiv;
          },
        });
        // 初始化G6图谱
        const graph = new G6.Graph({
          container: mount,
          center: true,
          // canvas的长宽
          width: mount.offsetWidth,
          height: mount.offsetHeight,
          plugins: [tooltip],
          // 设置可以拖动节点、放缩图谱等
          modes: {default: ['drag-canvas', 'drag-node']},
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
        // 读取数据、渲染图谱
        graph.data(this.graphData);
        graph.render();

        // 拖动节点的动画效果
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

        //单击节点事件（放大节点显示详情，再次单击则恢复）
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
          let labelText = model.oriLabel
          if (model.description.date && model.description.date !== '--') labelText += '\n 日期: ' + model.description.date + '\n';
          if (model.description.conductor && model.description.conductor !== '--') labelText += '执行者: ' + model.description.conductor + '\n';
          if (model.description.object && model.description.object !== '--') labelText += '处罚对象: ' + model.description.object + '\n';
          if (model.description.amount && model.description.amount !== '--') labelText += '金额: ' + model.description.amount + '\n';
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

      // echarts初始化
      initbargraph1() {
        let myChart = echarts.init(this.$refs.charts1, "macarons");
        myChart.setOption({
          title: {
            text: '历史持有盈利概率' + (this.pre_data.length > 0 ? '' : '(数据不足)'),
            textStyle: {
              fontSize: 20,
            }
            // subtext:'图例表示了在此知识图谱中，关系的类型与关系类型的分布情况'
          },
          grid: {
            top: 90
          },
          tooltip: {},
          xAxis: {
            data: this.pre_data_col
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
            text: '平均持有盈利情况' + (this.avg_data.length > 0 ? '' : '(数据不足)'),
            textStyle: {
              fontSize: 20,
            }
            // subtext:'图例表示了在此知识图谱中，关系的类型与关系类型的分布情况'
          },
          grid: {
            top: 90
          },
          tooltip: {},
          xAxis: {
            data: this.avg_data_col
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
    }
  }
</script>

<style scoped>
  #all {
    height: 100%;
    width: 85%;
    margin: 1em auto auto;
    border: 1px solid rgba(136, 136, 136, 0.54);
    border-radius: 20px;
  }

  #bar {
    margin-top: 3em;
    display: flex;
    /*line-height: 30px;*/
    height: 20px;
    align-items: center;
    min-width: 90%;
    /*background-color: aliceblue;*/
  }

  .headerContent {
    margin: -2.5em auto auto;
    font-size: 20px;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    padding: 40px;
    color: #636363;
  }

  #details {
    height: 94%;
    padding-top: 2%;
    padding-left: 3%;
    padding-right: 3%;
    width: 100%;
  }

  #text2 {
    font-size: 25px;
    font-weight: bold;
    /*padding-left: 7%;*/
    float: left;
  }

  #mount {
    text-align: center;
    /*margin: auto auto 3em;*/
    background-color: aliceblue;
    /*width: 70%;*/
    height: 450px;
    margin-bottom: 1em;
  }

  #chart {
    text-align: center;
    /*width: 80%;*/
    height: 80%;
  }

  .pin {
    float: right;
    font-weight: bold;
    margin-right: 1em;
  }

  img {
    height: 20px;
    width: 20px;
    margin-right: 10px;
  }

  .graph {
    margin-bottom: 3em;
    padding: 5px;
  }

  .g6-component-tooltip {
    background-color: rgba(255, 255, 255, 0.8);
    padding: 0px 10px 24px 10px;
  }

  .righttop {
    display: inline-block;
    /*margin: 3em;*/
    /*width: 80%;*/
    /*height: 80%;*/
  }
</style>
