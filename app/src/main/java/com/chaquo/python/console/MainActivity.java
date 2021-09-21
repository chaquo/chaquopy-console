package com.chaquo.python.console;

import android.app.*;
import com.chaquo.python.utils.*;

public class MainActivity extends PythonConsoleActivity {

    // On API level 31 and higher, pressing Back in a launcher activity sends it to the back by
    // default, but that would make it difficult to restart the activity.
    @Override public void onBackPressed() {
        finish();
    }

    @Override protected Class<? extends Task> getTaskClass() {
        return Task.class;
    }

    public static class Task extends PythonConsoleActivity.Task {
        public Task(Application app) {
            super(app);
        }

        @Override public void run() {
            py.getModule("main").callAttr("main");
        }
    }
}
