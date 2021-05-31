package com.example.stockgraph.vo;

import com.example.stockgraph.po.Event;
import com.example.stockgraph.po.Punish;
import com.example.stockgraph.po.Stock;

public class Node {
    private static int cur_id = 0;
    private int id;
    private String label;
    private String cluster;
    private Description description;

    public Node(Stock stock) {
        cur_id = 0;
        this.id = cur_id++;
        this.label = stock.getName();
        this.cluster = "股票";
        this.description = new Description();
    }

    public Node(Event event) {
        this.id = cur_id++;
        this.label = event.getLabel();
        this.cluster = "近期事件";
        this.description = new Description(event.getDate());
    }

    public Node(Punish punish) {
        this.id = cur_id++;
        this.label = punish.getLabel();
        this.cluster = "处罚事件";
        this.description = new Description(
                punish.getDate(),
                punish.getAmount(),
                punish.getConductor(),
                punish.getObject());
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public String getCluster() {
        return cluster;
    }

    public void setCluster(String cluster) {
        this.cluster = cluster;
    }

    public Description getDescription() {
        return description;
    }

    public void setDescription(Description description) {
        this.description = description;
    }
}
