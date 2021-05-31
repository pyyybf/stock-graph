package com.example.stockgraph.data;

import com.example.stockgraph.po.Punish;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Mapper
@Repository
public interface PunishMapper {
    List<Punish> getPunishByStockId(int stock_id);
}
