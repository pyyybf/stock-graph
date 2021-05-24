package com.example.stockgraph.po;

public class Stock {
    private int id;
    private String name;
    private double quarter_p;
    private double quarter_a;
    private double halfYear_p;
    private double halfYear_a;
    private double year_p;
    private double year_a;
    private double guarantee_a;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getQuarter_p() {
        return quarter_p;
    }

    public void setQuarter_p(double quarter_p) {
        this.quarter_p = quarter_p;
    }

    public double getQuarter_a() {
        return quarter_a;
    }

    public void setQuarter_a(double quarter_a) {
        this.quarter_a = quarter_a;
    }

    public double getHalfYear_p() {
        return halfYear_p;
    }

    public void setHalfYear_p(double halfYear_p) {
        this.halfYear_p = halfYear_p;
    }

    public double getHalfYear_a() {
        return halfYear_a;
    }

    public void setHalfYear_a(double halfYear_a) {
        this.halfYear_a = halfYear_a;
    }

    public double getGuarantee_a() {
        return guarantee_a;
    }

    public double getYear_p() {
        return year_p;
    }

    public void setYear_p(double year_p) {
        this.year_p = year_p;
    }

    public double getYear_a() {
        return year_a;
    }

    public void setYear_a(double year_a) {
        this.year_a = year_a;
    }

    public void setGuarantee_a(double guarantee_a) {
        this.guarantee_a = guarantee_a;
    }
}
