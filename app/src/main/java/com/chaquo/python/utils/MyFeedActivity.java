package com.chaquo.python.utils;

import android.app.Application;
import android.os.Bundle;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.widget.TextView;

import com.chaquo.python.console.R;

public class MyFeedActivity extends BacNetActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_feed);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

 //       FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
 //       fab.setOnClickListener(new View.OnClickListener() {
 //           @Override
 //           public void onClick(View view) {
 //               Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
 //                       .setAction("Action", null).show();
 //           }
 //       });

        Python py = Python.getInstance();
        TextView textView = (TextView) findViewById(R.id.text_content);
        PyObject x = py.getModule("my_feed");
        String y = x.callAttr("do").toString();
        textView.setText(y);
    }




    public static class Task extends DebugActivity.Task {
        public Task(Application app) {
            super(app);
        }

        @Override public void run() {
            py.getModule("main").callAttr("main");
        }
    }





    @Override
    protected Class<? extends Task> getTaskClass() {
        return Task.class;
    }
}
