package com.chaquo.python.console

import android.app.Application
import com.chaquo.python.utils.DebugActivity

class MainActivity : DebugActivity() {

    override fun getTaskClass(): Class<out Task?> {
        return Task::class.java
    }

    class Task(app: Application?) : DebugActivity.Task(app) {
        override fun run() {
            py.getModule("main").callAttr("main")
        }
    }
}




