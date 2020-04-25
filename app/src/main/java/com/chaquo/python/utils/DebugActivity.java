package com.chaquo.python.utils;

import android.app.*;
import android.os.*;
import android.util.*;
import androidx.lifecycle.*;
import com.chaquo.python.*;

/** Base class for a console-based activity that will run Python code. sys.stdout and sys.stderr
 * will be directed to the output view whenever the activity is resumed. If the Python code
 * caches their values, it can direct output to the activity even when it's paused.
 *
 * If STDIN_ENABLED is passed to the Task constructor, sys.stdin will also be redirected whenever
 * the activity is resumed. The input box will initially be hidden, and will be displayed the
 * first time sys.stdin is read. */
public abstract class DebugActivity extends ConsoleActivity {

    protected Task task;

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        task = ViewModelProviders.of(this).get(getTaskClass());
    }

    protected abstract Class<? extends Task> getTaskClass();

    @Override protected void onResume() {
        task.resumeStreams();
        super.onResume();  // Starts the task thread.
    }

    @Override protected void onPause() {
        super.onPause();
        if (! isChangingConfigurations()) {
            task.pauseStreams();
        }
    }

    // =============================================================================================

    public static class Task extends BacNetPythonTask {

        public Task(Application app) {
            super(app);
        }

        /** Create the thread from Python rather than Java, otherwise user code may be surprised
         * to find its Python Thread object marked as "dummy" and "daemon". */
        @Override protected void startThread(Runnable runnable) {
            PyObject console = py.getModule("chaquopy.utils.console");
            console.callAttr("start_thread", runnable);
        }

        public void resumeStreams() {
            if (stdin != null) {
                sys.put("stdin", stdin);
            }
            sys.put("stdout", stdout);
            sys.put("stderr", stderr);
        }

        public void pauseStreams() {
            if (realStdin != null) {
                sys.put("stdin", realStdin);
            }
            sys.put("stdout", realStdout);
            sys.put("stderr", realStderr);
        }

        @SuppressWarnings("unused")  // Called from Python
        public void onInputState(boolean blocked) {
            if (blocked) {
                inputEnabled.postValue(true);
            }
        }

        @Override public void onInput(String text) {
            if (text != null) {
                // Messages which are empty (or only consist of newlines) will not be logged.
                Log.i("python.stdin", text.equals("\n") ? " " : text);
            }
            stdin.callAttr("on_input", text);
        }

        @Override protected void onCleared() {
            super.onCleared();
            if (stdin != null) {
                onInput(null);  // Signals EOF
            }
        }
    }

}
