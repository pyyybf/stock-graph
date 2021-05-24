package com.example.stockgraph.bl;

import com.example.stockgraph.po.Event;

import java.util.List;

public interface EventService {
    List<Event> getEventByStockId(int stock_id);
}
