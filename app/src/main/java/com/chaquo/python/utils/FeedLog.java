package com.chaquo.python.utils;

public class FeedLog {
    public String log_name;
    public String log_name_old;
    public String log_content;
    public String type;
    public String timestamp;


    private FeedLog() {
    }

    public static FeedLog postLog(String name, String content, String timestamp) {
        FeedLog f = new FeedLog();
        f.log_name = name;
        f.log_name_old = null;
        f.type = "post";
        f.log_content = content;
        f.timestamp = timestamp;
        return f;
    }

    public static FeedLog usernameLog(String old, String new_, String timestamp) {
        FeedLog f = new FeedLog();
        f.log_name = new_;
        f.log_name_old = old;
        f.type = "username";

        if(old.equals("")){
           f.log_content = "A new user just joined BACnet++!";
        }
        else {
            f.log_content = old + " changed their username to " + new_ + ". ";
        }

        f.timestamp = timestamp;
        return f;
    }

}
