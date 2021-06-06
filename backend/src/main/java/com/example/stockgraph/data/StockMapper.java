package com.example.stockgraph.data;

import com.example.stockgraph.po.Stock;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

@Mapper
@Repository
public interface StockMapper {
    Stock getStockById(int id);

    Stock getStockByName(String name);

    int ifExistId(int id);

    int ifExistName(String name);
}
