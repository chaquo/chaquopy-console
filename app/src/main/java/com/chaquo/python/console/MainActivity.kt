package com.chaquo.python.console

import android.app.Application
import com.chaquo.python.utils.PythonConsoleActivity

class MainActivity : PythonConsoleActivity() {
    override fun getTaskClass(): Class<out Task?> {
        return Task::class.java
    }

    class Task(app: Application?) : PythonConsoleActivity.Task(app) {
        override fun run() {
            py.getModule("main").callAttr("main")
        }
    }
}