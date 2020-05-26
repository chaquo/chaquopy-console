package com.chaquo.python.utils;

public class Person {
    public int master_idx;
    public String name;
    public int feed_id_idx;
    public String feed_id;
    public boolean trusted;

    public Person(int master_idx, String name, int feed_id_idx, String feed_id, boolean trusted) {
        this.master_idx = master_idx;
        this.name = name;
        this.feed_id_idx = feed_id_idx;
        this.feed_id = feed_id;
        this.trusted = trusted;
    }

    @Override
    public String toString(){
        String s = "Person with: \n";
        s += "master_idx: " + master_idx + "\n";
        s += "name: " + name+ "\n";
        s += "feed_id_idx: " + feed_id_idx+ "\n";
        s += "feed_id: " + feed_id+ "\n";
        s += "trusted?: " + trusted+ "\n";
        return s;
    }




}