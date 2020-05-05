package com.chaquo.python.utils;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.Application;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.PopupWindow;

import com.chaquo.python.console.R;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

public class RecyclerFeedActivity extends BacNetActivity {
    private RecyclerView recyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;


    public void openSendMessageActivity(){
        LayoutInflater inflater = (LayoutInflater)
                getSystemService(LAYOUT_INFLATER_SERVICE);
        View popupView = inflater.inflate(R.layout.activity_send_message, null);

        // create the popup window
        //int width = LinearLayout.LayoutParams.WRAP_CONTENT;
        int height = LinearLayout.LayoutParams.WRAP_CONTENT;
        int width = 800;
        //int height = 950;
        boolean focusable = true; // lets taps outside the popup also dismiss it
        final PopupWindow popupWindow = new PopupWindow(popupView, width, height, focusable);

        // show the popup window
        // which view you pass in doesn't matter, it is only used for the window tolken
        popupWindow.showAtLocation(recyclerView, Gravity.CENTER, 0, -100);

        // dismiss the popup window when touched
        /*
        popupView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                popupWindow.dismiss();
                return true;
            }
        });
         */
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recycler_feed);
        recyclerView = (RecyclerView) findViewById(R.id.my_recycler_view);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.floatingActionButton2);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openSendMessageActivity();
            }
        });

        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        recyclerView.setHasFixedSize(true);

        // use a linear layout manager
        layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);

        // specify an adapter (see also next example)
        FeedLog f1 = new FeedLog("ben hur har hir", "hello world TableLayout positions its children into rows and columns. TableLayout containers do not display border lines for their rows, columns, or cells. The table will have as many columns as the row with the most cells. A table can leave cells empty.  Cells can span  multiple columns, as they can in HTML. You can span columns by using the span field in the TableRow.LayoutParams class.  ", "10:15");
        FeedLog f2 = new FeedLog("lara", "hi there", "11:15");
        FeedLog f3 = new FeedLog("snaja", "As dawn breaks he enters " +
                "A room with the odor of acid. " +
                "He lays the copper plate on the table. " +
                "And reaches for the shaft of the burin. " +
                "Dublin wakes to horses and rain. " +
                "Street hawkers call. " +
                "All the news is famine and famine. " +
                "The flat graver, the round graver, " +
                "The angle tint tool wait for him. " +
                "He bends to his work and begins. " +
                "He starts with the head, cutting in " +
                "To the line of the cheek, finding " +
                "The slope of the skull, incising " +
                "The shape of a face that becomes " +
                "A foundry of shadows, rendering — " +
                "With a deeper cut into copper — " +
                "The whole woman as a skeleton, " +
                "The rags of  her skirt, her wrist " +
                "In a bony line forever " +
                "                                        severing " +
                "Her body from its native air until " +
                "She is ready for the page, " +
                "For the street vendor, for " +
                "A new inventory which now " +
                "To loss and to laissez-faire adds " +
                "The odor of acid and the little, " +
                "Pitiless tragedy of  being imagined. " +
                "He puts his tools away, " +
                "One by one; lays them out carefully " +
                "On the deal table, his work done.", "12:15");
        FeedLog f4 = new FeedLog("nour", "As dawn breaks he enters " +
                "A room with the odor of acid. " +
                "He lays the copper plate on the table. " +
                "And reaches for the shaft of the burin. " +
                "Dublin wakes to horses and rain. " +
                "Street hawkers call. " +
                "All the news is famine and famine. " +
                "The flat graver, the round graver, " +
                "The angle tint tool wait for him. " +
                "He bends to his work and begins. " +
                "He starts with the head, cutting in " +
                "To the line of the cheek, finding " +
                "The slope of the skull, incising " +
                "The shape of a face that becomes " +
                "A foundry of shadows, rendering — " +
                "With a deeper cut into copper — " +
                "The whole woman as a skeleton, " +
                "The rags of  her skirt, her wrist " +
                "In a bony line forever " +
                "                                        severing " +
                "Her body from its native air until " +
                "She is ready for the page, " +
                "For the street vendor, for " +
                "A new inventory which now " +
                "To loss and to laissez-faire adds " +
                "The odor of acid and the little, " +
                "Pitiless tragedy of  being imagined. " +
                "He puts his tools away, " +
                "One by one; lays them out carefully " +
                "On the deal table, his work done.", "12:24");

        mAdapter = new MyFeedAdapter(new FeedLog[] {f1, f2, f3, f4}); // TODO !!!
        recyclerView.setAdapter(mAdapter);
    }


    public static class Task extends DebugActivity.Task {
        public Task(Application app) {
            super(app);
        }

        @Override public void run() {
            py.getModule("main").callAttr("main");
        } //TODO
    }

    @Override
    protected Class<? extends Task> getTaskClass() {
        return Task.class;
    }
}
