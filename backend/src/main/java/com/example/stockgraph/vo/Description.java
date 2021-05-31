package com.example.stockgraph.vo;

public class Description {
    private String date;
    private String amount;
    private String conductor;
    private String object;

    public Description() {
    }

    public Description(String date) {
        this.date = date;
        this.amount = "--";
        this.conductor = "--";
        this.object = "--";
    }

    public Description(String date, String amount, String conductor, String object) {
        this.date = date;
        this.amount = amount;
        this.conductor = conductor;
        this.object = object;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getAmount() {
        return amount;
    }

    public void setAmount(String amount) {
        this.amount = amount;
    }

    public String getConductor() {
        return conductor;
    }

    public void setConductor(String conductor) {
        this.conductor = conductor;
    }

    public String getObject() {
        return object;
    }

    public void setObject(String object) {
        this.object = object;
    }
}
