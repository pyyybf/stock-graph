<template>
  <div id="all">
    <!-- {{$data.currentStockName}} -->
    <div id="bar">
      <div id="StockName">{{$data.currentStockName}} 深圳机场</div>
      <div id="StockId">Id {{$data.currentStockId}}</div>
      <div id="Guarantee">
        <div id="text">总担保额</div>
        <div id="Num">￥{{$data.guarantee_a.toFixed(2)}}</div>
      </div>
    </div>

    <div id="details">
      <!-- echarts -->
      <div id="echarts">
        <a-row id="chart">
          <a-col :span="12">
            <div class="righttop" ref="charts1" style="height: 500px;width:500px;padding-left:15%"></div>
          </a-col>
          <a-col :span="12">
            <div class="righttop" ref="charts2" style="height: 500px;width:500px；padding-right:15%"></div>
          </a-col>
        </a-row>
      </div>
      <div id="text2">近期事件与处罚事件</div>
      <div id="legend">
        <div id="green"><img src="../assets/circle.png" style="height:35px;width:35px"/>  股票</div>
        <div id="red"><img src="../assets/circle2.png" style="height:35px;width:35px"/>   处罚事件</div>
        <div id="blue"><img src="../assets/circle3.png" style="height:35px;width:35px"/>   近期事件</div>        
      </div>
      <!--挂载G6图谱-->
      <div id="mount"></div>
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
        pre_data: [5,3,23],
        avg_data: [1,1,1],
        guarantee_a:0,
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
        this.pre_data[0] = res.data.content.stock.quarter_p;
        this.pre_data[1] = res.data.content.stock.halfYear_p;
        this.pre_data[2] = res.data.content.stock.year_p;
        this.avg_data = [];
        this.avg_data[0] = res.data.content.stock.quarter_a;
        this.avg_data[1] = res.data.content.stock.halfYear_a;
        this.avg_data[2] = res.data.content.stock.year_a;
        this.guarantee_a=res.data.content.stock.guarantee_a;
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
        this.guarantee_a=res.data.content.stock.guarantee_a;
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
            if(e.item.getModel().index === 0) outDiv.innerHTML = e.item.getModel().label;
            else outDiv.innerHTML = e.item.getModel().description.date;
            return outDiv;
          },
        });
        // 初始化G6图谱
        const graph = new G6.Graph({
          container: mount,
          center: true,
          // canvas的长宽
          width: 1000,
          height: 500,
          plugins: [tooltip],
          // 设置可以拖动节点、放缩图谱等
          modes: {default: ['zoom-canvas', 'drag-canvas', 'drag-node']},
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
          let labelText = model.oriLabel + '\n Date: ' + model.description.date + '\n';
          if (model.description.conductor !== '--') labelText += 'Conductor: ' + model.description.conductor + '\n';
          if (model.description.amount !== '--') labelText += 'Amount: ' + model.description.amount + '\n';
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
            text: '历史持有盈利概率',
            textStyle:{
              fontSize:25,
            }
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
            text: '平均持有盈利情况',
            textStyle:{
              fontSize:25,
            }
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
    }
  }
</script>

<style scoped>
  #all{
    height: 100%;
    width: 100%;
  }
  #bar{
    width: 100%;
    height: 5%;
    display: flex;
    background-color: rgba(77, 130, 251, 0.75);
    /* position: fixed;
    top:0;
    left: 0;
    right: 0; */
  }
  #StockName{
    width: 20%;
    height: 70%;
    font-size: 43px;
    margin-bottom: 0.5%;
    padding-left: 30px;
    color:whitesmoke;
    font-weight: bold;
    
  }
  #StockId{
    width: 20%;
    height: 70%;
    font-size: 43px;
    margin-bottom: 0.5%;
    padding-left: 30px;
    color:whitesmoke;
    /* font-weight: bold; */

  }
  #Guarantee{
    width:60%;
    height: 100%;
    display: flex;
  }
  #text{
    width: 35%;
    height: 70%;
    font-size: 40px;
    margin-bottom: 0.5%;
    margin-left: 40%;
    padding-left: 30px;
    color:whitesmoke;
  }
  #Num{
    width: 35%;
    font-size: 43px;
    margin-bottom: 0.5%;
    margin-bottom: 10px;
    color:red;
  }
  #details{
    height: 94%;
    padding-top: 2%;
    padding-left: 3%;
    padding-right: 3%;
    width: 100%;
    background-color: aliceblue;
  }
  #text2{
    font-size: 25px;
    font-weight: bold;
    padding-left: 8%;
    width: 30%;
    float: left;
  }
  #mount {
    background-color: aliceblue;
    width: 100%;
    padding-left: 100px;
  }
  #chart {
    background-color: aliceblue;
    width: 100%;
  }
  #green,#red,#blue{
    width: 15%;
    float:right;
    font-weight: bold;
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
