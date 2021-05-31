package com.example.stockgraph.blImpl;

import com.example.stockgraph.bl.PunishService;
import com.example.stockgraph.data.PunishMapper;
import com.example.stockgraph.po.Punish;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PunishServiceImpl implements PunishService {
    @Autowired
    PunishMapper punishMapper;

    @Override
    public List<Punish> getPunishByStockId(int stock_id) {
        return punishMapper.getPunishByStockId(stock_id);
    }
}
