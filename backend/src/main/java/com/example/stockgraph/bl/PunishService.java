package com.example.stockgraph.bl;

import com.example.stockgraph.po.Punish;

import java.util.List;

public interface PunishService {
    List<Punish> getPunishByStockId(int stock_id);
}
