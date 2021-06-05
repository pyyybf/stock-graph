package com.example.stockgraph.controller;

import com.example.stockgraph.bl.EventService;
import com.example.stockgraph.bl.PunishService;
import com.example.stockgraph.bl.StockService;
import com.example.stockgraph.po.Event;
import com.example.stockgraph.po.Punish;
import com.example.stockgraph.po.Stock;
import com.example.stockgraph.vo.GraphInfo;
import com.example.stockgraph.vo.ResponseVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController()
@RequestMapping("/api/stock")
public class StockController {
    @Autowired
    StockService stockService;
    @Autowired
    EventService eventService;
    @Autowired
    PunishService punishService;

    @GetMapping("/getStockById")
    public ResponseVO getStockById(@RequestParam(value = "id") int id) {
        GraphInfo graphInfo = new GraphInfo(
                stockService.getStockById(id),
                eventService.getEventByStockId(id),
                punishService.getPunishByStockId(id));
        return ResponseVO.buildSuccess(graphInfo);
    }

    @GetMapping("/getStockByName")
    public ResponseVO getStockByName(@RequestParam(value = "name") String name) {
        Stock stock = stockService.getStockByName(name);
        GraphInfo graphInfo = new GraphInfo(
                stock,
                eventService.getEventByStockId(stock.getId()),
                punishService.getPunishByStockId(stock.getId()));
        return ResponseVO.buildSuccess(graphInfo);
    }

    @GetMapping("/ifExist")
    public ResponseVO ifExist(@RequestParam(value = "id") int id, @RequestParam(value = "name") String name) {
        return ResponseVO.buildSuccess(stockService.ifExist(id, name) > 0);
    }
}
