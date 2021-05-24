package com.example.stockgraph.controller;

import com.example.stockgraph.bl.StockService;
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

    @GetMapping("/getStockById")
    public ResponseVO getStockById(@RequestParam(value = "id") int id) {
        return ResponseVO.buildSuccess(stockService.getStockById(id));
    }

    @GetMapping("/getStockByName")
    public ResponseVO getStockByName(@RequestParam(value = "name") String name) {
        return ResponseVO.buildSuccess(stockService.getStockByName(name));
    }
}
