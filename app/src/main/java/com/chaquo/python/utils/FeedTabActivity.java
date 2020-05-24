package com.chaquo.python.utils;

import android.app.Application;
import android.os.Bundle;

import com.chaquo.python.Python;
import com.chaquo.python.console.R;
import com.chaquo.python.utils.ui.main.MyFeedTab;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.android.material.tabs.TabLayout;

import androidx.recyclerview.widget.RecyclerView;
import androidx.viewpager.widget.ViewPager;
import androidx.appcompat.app.AppCompatActivity;

import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import com.chaquo.python.utils.ui.main.SectionsPagerAdapter;

public class FeedTabActivity extends BacNetActivity {
    //private RecyclerView myFeedTab;
    //private RecyclerView.Adapter mAdapter;
    //private RecyclerView.LayoutManager layoutManager;
    protected Python py = Python.getInstance();
    public boolean run = true;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_feed_tab);
        if (run) {
            py.getModule("kotlin_db_cbor_event").callAttr("start");
            run = false;
        }
        //myFeedTab = findViewById(R.id.my_feed_recycle_tab);
        SectionsPagerAdapter sectionsPagerAdapter = new SectionsPagerAdapter(this, getSupportFragmentManager());

        ViewPager viewPager = findViewById(R.id.view_pager);
        viewPager.setAdapter(sectionsPagerAdapter);
        TabLayout tabs = findViewById(R.id.tabs);
        tabs.setupWithViewPager(viewPager);

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
    protected Class<? extends RecyclerFeedActivity.Task> getTaskClass() {
        return RecyclerFeedActivity.Task.class;
    }
}
