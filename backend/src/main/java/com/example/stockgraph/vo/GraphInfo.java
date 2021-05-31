package com.example.stockgraph.vo;

import com.example.stockgraph.po.Event;
import com.example.stockgraph.po.Punish;
import com.example.stockgraph.po.Stock;

import java.util.ArrayList;
import java.util.List;

public class GraphInfo {
    private Stock stock;
    private List<Node> nodes;
    private List<Edge> edges;

    public GraphInfo(Stock stock, List<Event> eventList, List<Punish> punishList) {
        this.stock = stock;
        this.nodes = new ArrayList<>();
        this.edges = new ArrayList<>();
        nodes.add(new Node(stock));
        for (Event event : eventList) {
            Node node = new Node(event);
            nodes.add(node);
            edges.add(new Edge(0, node.getId()));
        }
        for (Punish punish : punishList) {
            Node node = new Node(punish);
            nodes.add(node);
            edges.add(new Edge(0, node.getId()));
        }
    }

    public Stock getStock() {
        return stock;
    }

    public void setStock(Stock stock) {
        this.stock = stock;
    }

    public List<Node> getNodes() {
        return nodes;
    }

    public void setNodes(List<Node> nodes) {
        this.nodes = nodes;
    }

    public List<Edge> getEdges() {
        return edges;
    }

    public void setEdges(List<Edge> edges) {
        this.edges = edges;
    }
}
