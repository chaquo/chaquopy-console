package com.chaquo.python.utils;

import android.annotation.SuppressLint;
import android.app.Application;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.PopupWindow;

import androidx.annotation.RequiresApi;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.console.R;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.util.Arrays;
import java.util.Collections;

public class FriendslistActivity extends BacNetActivity {
    private RecyclerView recyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;




    @SuppressLint("ResourceType")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_friendslist);
        recyclerView = (RecyclerView) findViewById(R.id.my_recycler_view);



        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        recyclerView.setHasFixedSize(true);

        // use a linear layout manager
        layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);

        // specify an adapter (see also next example)
        passFriendsToGUI();

    }

    public void passFriendsToGUI() {
        /*
        Person p1 = new Person("Travis");
        Person p2 = new Person("Nour");
        Person p3 = new Person("Sanja");
        Person[] p = {p1, p2, p3};
        */


        Python py = Python.getInstance();
        PyObject x = py.getModule("kotlin_db_cbor_event");
        String[] y = x.callAttr("get_all_usernames").toJava(String[].class);

        Person[] persons = new Person[y.length];

        for(int i = 0; i < y.length; i++){
                String name = y[i];
                persons[i]  = new Person(name);
        }

        Collections.reverse(Arrays.asList(persons));

        mAdapter = new PersonListAdapter(persons);
        recyclerView.setAdapter(mAdapter);
    }

    @Override
    protected void onResume() {
        super.onResume();
        passFriendsToGUI();
    }

    public static class Task extends DebugActivity.Task {
        public Task(Application app) {
            super(app);
        }

        @Override
        public void run() {
            py.getModule("main").callAttr("main");
        } //TODO
    }

    @Override
    protected Class<? extends Task> getTaskClass() {
        return Task.class;
    }
}

