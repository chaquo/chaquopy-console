package com.chaquo.python.utils;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.Application;
import android.os.Bundle;

import com.chaquo.python.console.R;

public class RecyclerFeedActivity extends BacNetActivity {
    private RecyclerView recyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recycler_feed);
        recyclerView = (RecyclerView) findViewById(R.id.my_recycler_view);

        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        recyclerView.setHasFixedSize(true);

        // use a linear layout manager
        layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);

        // specify an adapter (see also next example)
        FeedLog f1 = new FeedLog("ben hur har hir", "hello world\nTableLayout positions its children into rows and columns. TableLayout containers do not display border lines for their rows, columns, or cells. The table will have as many columns as the row with the most cells. A table can leave cells empty. \nCells can span\n multiple columns, as they can in HTML. You can span columns by using the span field in the TableRow.LayoutParams class.  ", "10:15");
        FeedLog f2 = new FeedLog("lara", "hi there", "11:15");
        FeedLog f3 = new FeedLog("snaja", "As dawn breaks he enters\n" +
                "A room with the odor of acid.\n" +
                "He lays the copper plate on the table.\n" +
                "And reaches for the shaft of the burin.\n" +
                "Dublin wakes to horses and rain.\n" +
                "Street hawkers call.\n" +
                "All the news is famine and famine.\n" +
                "The flat graver, the round graver,\n" +
                "The angle tint tool wait for him.\n" +
                "He bends to his work and begins.\n" +
                "He starts with the head, cutting in\n" +
                "To the line of the cheek, finding\n" +
                "The slope of the skull, incising\n" +
                "The shape of a face that becomes\n" +
                "A foundry of shadows, rendering —\n" +
                "With a deeper cut into copper —\n" +
                "The whole woman as a skeleton,\n" +
                "The rags of  her skirt, her wrist\n" +
                "In a bony line forever\n" +
                "                                        severing\n" +
                "Her body from its native air until\n" +
                "She is ready for the page,\n" +
                "For the street vendor, for\n" +
                "A new inventory which now\n" +
                "To loss and to laissez-faire adds\n" +
                "The odor of acid and the little,\n" +
                "Pitiless tragedy of  being imagined.\n" +
                "He puts his tools away,\n" +
                "One by one; lays them out carefully\n" +
                "On the deal table, his work done.", "12:15");
        mAdapter = new MyFeedAdapter(new FeedLog[] {f1, f2, f3}); // TODO !!!
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
