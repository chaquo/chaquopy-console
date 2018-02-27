from android.os import Bundle
from android.support.v7.app import AppCompatActivity
from com.chaquo.python.hello import R
from java import jvoid, Override, static_proxy


class MainActivity(static_proxy(AppCompatActivity)):

    @Override(jvoid, [Bundle])
    def onCreate(self, state):
        AppCompatActivity.onCreate(self, state)
        self.setContentView(R.layout.activity_main)
