package com.example.stockgraph.bl;

import com.example.stockgraph.po.Stock;

public interface StockService {
    Stock getStockById(int id);

    Stock getStockByName(String name);

    int ifExistId(int id);

    int ifExistName(String name);
}
