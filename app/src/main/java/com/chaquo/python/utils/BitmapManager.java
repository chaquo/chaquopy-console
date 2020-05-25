package com.chaquo.python.utils;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;

import java.io.ByteArrayOutputStream;

public class BitmapManager {

    public static final String SEPARATOR = "|";

    // don't let ANYONE instantiate this class
    private BitmapManager(){
        ;
    }

    public static String fromBitMapToString(Bitmap bitmap){
        ByteArrayOutputStream baos=new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG,10, baos);
        byte [] b=baos.toByteArray();
        String temp= Base64.encodeToString(b, Base64.DEFAULT);
        return temp;
    }

    public static Bitmap fromStringToBitmap(String string){
        try {
            byte [] encodeByte=Base64.decode(string,Base64.DEFAULT);
            Bitmap bitmap= BitmapFactory.decodeByteArray(encodeByte, 0, encodeByte.length);
            bitmap = Bitmap.createScaledBitmap(bitmap, 250, 250, false);
            return bitmap;
        } catch(Exception e) {
            e.getMessage();
            return null;
        }
    }
}
