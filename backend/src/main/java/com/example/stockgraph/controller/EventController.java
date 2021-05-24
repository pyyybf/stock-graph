package com.example.stockgraph.controller;

import com.example.stockgraph.bl.EventService;
import com.example.stockgraph.vo.ResponseVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController()
@RequestMapping("/api/event")
public class EventController {
    @Autowired
    EventService eventService;

    @GetMapping("/getEventByStockId")
    public ResponseVO getEventByStockId(@RequestParam(value = "stock_id") int stock_id) {
        return ResponseVO.buildSuccess(eventService.getEventByStockId(stock_id));
    }
}
