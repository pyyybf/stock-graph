<template>
  <div class="">

    <div id="mount"></div>

  </div>
</template>

<script>
  import {getStockByIdAPI, getStockByNameAPI} from "../api";
  import G6 from '@antv/g6';

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
  // const colors = [
  //   '#BDD2FD',
  //   '#BDEFDB',
  //   '#C2C8D5',
  //   '#FBE5A2',
  //   '#F6C3B7',
  //   '#B6E3F5',
  //   '#D3C6EA',
  //   '#FFD8B8',
  //   '#AAD8D8',
  //   '#FFD6E7',
  // ];
  // const strokes = [
  //   '#5B8FF9',
  //   '#5AD8A6',
  //   '#5D7092',
  //   '#F6BD16',
  //   '#E8684A',
  //   '#6DC8EC',
  //   '#9270CA',
  //   '#FF9D4D',
  //   '#269A99',
  //   '#FF99C3',
  // ];
  export default {
    name: "StockDetail",
    data() {
      return {
        currentStockId: -1,
        currentStockName: '',
        graphData:{}
      }
    },
    async mounted() {
      if (this.$route.params.stockId) {
        this.currentStockId = this.$route.params.stockId;
        const res = await getStockByIdAPI(this.currentStockId);
        console.log(res.data.content) //包含stock，nodes，edges
        this.graphData = res.data.content;
        this.graphData.nodes.forEach((node) => {
          node.id = node.id.toString();
        });
        this.graphData.edges.forEach((edge) => {
          edge.source = edge.source.toString();
          edge.target = edge.target.toString();
        });
      } else {
        this.currentStockName = this.$route.params.stockName;
        const res = await getStockByNameAPI(this.currentStockName);
        // console.log(res.data.content);
        this.graphData = res.data.content;
        this.graphData.nodes.forEach((node) => {
          node.id = node.id.toString();
        });
        this.graphData.edges.forEach((edge) => {
          edge.source = edge.source.toString();
          edge.target = edge.target.toString();
        });

      }
      this.init();
    },
    methods: {
      init(){
        const mount = document.getElementById('mount');
        this.graphData.nodes.forEach((node) => {
          node.style = {};
          if(node.cluster === '股票') {node.style.fill = colors[0]; node.size = 60;}
          else if(node.cluster === '近期事件') node.style.fill = colors[1];
          else node.style.fill = colors[2];
        });
        const graph = new G6.Graph({
          container: mount,
          center: true,
          width: 600,
          height: 500,
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

      },



    },
  }
</script>

<style scoped>
#mount{
  background-color: aliceblue;
}
</style>
