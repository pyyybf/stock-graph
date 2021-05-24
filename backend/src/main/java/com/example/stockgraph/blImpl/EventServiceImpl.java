package com.example.stockgraph.blImpl;

import com.example.stockgraph.bl.EventService;
import com.example.stockgraph.data.EventMapper;
import com.example.stockgraph.po.Event;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EventServiceImpl implements EventService {
    @Autowired
    EventMapper eventMapper;

    @Override
    public List<Event> getEventByStockId(int stock_id) {
        return eventMapper.getEventByStockId(stock_id);
    }
}
