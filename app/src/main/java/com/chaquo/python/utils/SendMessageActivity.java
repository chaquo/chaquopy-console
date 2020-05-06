package com.chaquo.python.utils;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.chaquo.python.console.R;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
//functionless
public class SendMessageActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send_message);
        Log.d("HERE", "IN SEND MESSAGE ACTIVITY");
        Button fab = (Button) findViewById(R.id.post_button);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                //append to feed
                postContent();
            }
        });
    }
    void postContent() {
        EditText receiver = findViewById(R.id.send_message_to);
        EditText message = findViewById(R.id.send_post_content);
        String audience = receiver.getText().toString();
        String content = message.getText().toString();
        //Log.d("HERE", audience);
        System.out.println(audience);
        //Log.d("HERE", content);
    }
}
