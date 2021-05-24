package com.example.stockgraph.data;

import com.example.stockgraph.po.Event;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Mapper
@Repository
public interface EventMapper {
    List<Event> getEventByStockId(int stock_id);
}
