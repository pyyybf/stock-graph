package com.example.stockgraph.blImpl;

import com.example.stockgraph.bl.StockService;
import com.example.stockgraph.data.StockMapper;
import com.example.stockgraph.po.Stock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class StockServiceImpl implements StockService {
    @Autowired
    StockMapper stockMapper;

    @Override
    public Stock getStockById(int id) {
        return stockMapper.getStockById(id);
    }

    @Override
    public Stock getStockByName(String name) {
        return stockMapper.getStockByName(name);
    }
}
