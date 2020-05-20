package com.chaquo.python.utils.ui.main;

import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.PopupWindow;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.console.R;
import com.chaquo.python.utils.FeedLog;
import com.chaquo.python.utils.MyFeedAdapter;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.util.Arrays;
import java.util.Collections;

import static android.content.Context.LAYOUT_INFLATER_SERVICE;

public class MyFeedTab extends Fragment {
    private View v;
    private RecyclerView recyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    public void openSendMessageActivity() {
        LayoutInflater inflater = (LayoutInflater) getActivity().getSystemService(LAYOUT_INFLATER_SERVICE);
        final View popupView = inflater.inflate(R.layout.activity_send_message, null);
        // create the popup window
        //int width = LinearLayout.LayoutParams.WRAP_CONTENT;
        int height = LinearLayout.LayoutParams.WRAP_CONTENT;
        int width = 700;
        //int height = 950;
        boolean focusable = true; // lets taps outside the popup also dismiss it
        final PopupWindow popupWindow = new PopupWindow(popupView, width, height, focusable);
        popupWindow.setElevation(50);
        popupWindow.setTouchable(true);
        // show the popup window
        // which view you pass in doesn't matter, it is only used for the window tolken
        popupWindow.showAtLocation(recyclerView, Gravity.CENTER, 0, -100);
        Button button = popupView.findViewById(R.id.post_button);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                //append to feed
                EditText receiver = popupView.findViewById(R.id.send_message_to);
                EditText message = popupView.findViewById(R.id.send_post_content);
                String audience = receiver.getText().toString();
                String content = message.getText().toString();
                postContent(audience, content);
                popupWindow.dismiss();
                //System.out.println("CLICKED ON BUTTON");
            }
        });
    }

    void postContent(String audience, String content) {
        System.out.println(audience);
        //call python
        /*
        Python py = Python.getInstance();
        PyObject x = py.getModule("main");
        x.callAttr("append", content);
        passLogToGUI();
         */
        Python py = Python.getInstance();
        PyObject x = py.getModule("database.appconn.kotlin_connection");
        x.callAttr("create_db");
    }




    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        v = inflater.inflate(R.layout.my_feed_tab, container, false);
        recyclerView = v.findViewById(R.id.my_feed_recycle_tab);
        recyclerView.setHasFixedSize(true);

        FloatingActionButton fab = (FloatingActionButton) v.findViewById(R.id.send_mssg);
        fab.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
            @Override
            public void onClick(View view) {
                openSendMessageActivity();
            }
        });


        layoutManager = new LinearLayoutManager(getActivity());
        recyclerView.setLayoutManager(layoutManager);
        passLogToGUI();
        return v;
    }

    public void passLogToGUI() {

        Python py = Python.getInstance();
        PyObject x = py.getModule("main");
        String entries = x.callAttr("dumpList").toString();
        //we have to pass array with string [content|sequence] as array
        String[] s = entries.split("_"); // s = ["content1, seq1, content2, seq2, content3...]
        //Log.d("informations2", Arrays.toString(s));
        FeedLog[] feed = new FeedLog[s.length / 2];
        for (int i = s.length / 2 - 1; i >= 0; i--) {
            FeedLog entry = new FeedLog("", s[i * 2], s[i * 2 + 1]);
            feed[s.length / 2 - i - 1] = entry;
            //Log.d("informations2", feed[s.length/2-i-1].log_content);
        }
        Collections.reverse(Arrays.asList(feed));

        mAdapter = new MyFeedAdapter(feed);
        recyclerView.setAdapter(mAdapter);
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }
}
