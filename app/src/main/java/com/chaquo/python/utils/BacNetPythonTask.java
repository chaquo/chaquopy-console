package com.chaquo.python.utils;

import android.app.Application;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

public class BacNetPythonTask extends ConsoleActivity.Task{
    protected Python py = Python.getInstance();
    protected PyObject sys;
    protected PyObject stdin, stdout, stderr;
    protected PyObject realStdin, realStdout, realStderr;

    public static final int STDIN_DISABLED = 0x0, STDIN_ENABLED = 0x1;
    public BacNetPythonTask(Application app) { this(app, STDIN_ENABLED); }

    public BacNetPythonTask(Application app, int flags) {
        super(app);
        sys = py.getModule("sys");
        PyObject console = py.getModule("chaquopy.utils.console");
        if ((flags & STDIN_ENABLED) != 0) {
            realStdin = sys.get("stdin");
            stdin = console.callAttr("ConsoleInputStream", this);
        }

        realStdout = sys.get("stdout");
        realStderr = sys.get("stderr");
        stdout = console.callAttr("ConsoleOutputStream", this, "output", realStdout);
        stderr = console.callAttr("ConsoleOutputStream", this, "outputError", realStderr);
    }

    @Override public void run() {
        py.getModule("main").callAttr("main");
    }
}
