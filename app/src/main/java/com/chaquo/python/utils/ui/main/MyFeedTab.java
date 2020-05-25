package com.chaquo.python.utils.ui.main;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
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
import com.chaquo.python.utils.AccountActivity;
import com.chaquo.python.utils.BitmapManager;
import com.chaquo.python.utils.FeedLog;
import com.chaquo.python.utils.MyFeedAdapter;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.io.FileNotFoundException;
import java.io.InputStream;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;

import static android.app.Activity.RESULT_OK;
import static android.content.Context.LAYOUT_INFLATER_SERVICE;

public class MyFeedTab extends Fragment {

    private View v;
    private RecyclerView recyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;
    private static int RESULT_LOAD_IMAGE = 1;
    private Bitmap bitmap;

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
                EditText message = popupView.findViewById(R.id.send_post_content);
                String content = message.getText().toString();
                if(bitmap != null){
                    //String s = Huffmann.encode(BitmapManager.fromBitMapToString(bitmap));
                    String s = BitmapManager.fromBitMapToString(bitmap);
                    content = BitmapManager.SEPARATOR + content + BitmapManager.SEPARATOR + s;
                }
                postContent(content);
                popupWindow.dismiss();
                bitmap = null;
                //System.out.println("CLICKED ON BUTTON");
            }
        });

        Button add_img = popupView.findViewById(R.id.add_img);
        add_img.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                getImg();
            }
        });
    }


    public void getImg(){
        Intent photoPickerIntent = new Intent(Intent.ACTION_PICK);
        photoPickerIntent.setType("image/*");
        startActivityForResult(photoPickerIntent, MyFeedTab.RESULT_LOAD_IMAGE);
    }

    @Override
    public void onActivityResult(int reqCode, int resultCode, Intent data) {
        super.onActivityResult(reqCode, resultCode, data);

        if (resultCode == RESULT_OK) {
            try {
                final Uri imageUri = data.getData();
                final InputStream imageStream = getActivity().getContentResolver().openInputStream(imageUri);
                bitmap = BitmapFactory.decodeStream(imageStream);
                bitmap = Bitmap.createScaledBitmap(
                        bitmap, 100, 100, false);
                //image_view.setImageBitmap(selectedImage);
            } catch (FileNotFoundException e) {
            }

        }else {
            //Toast.makeText(PostImage.this, "You haven't picked Image",Toast.LENGTH_LONG).show();
        }
    }


    void postContent(String content) {
        //call python
        /*
        Python py = Python.getInstance();
        PyObject x = py.getModule("main");
        x.callAttr("append", content);
        passLogToGUI();
         */
        Python py = Python.getInstance();
        //PyObject x = py.getModule("database.appconn.kotlin_connection");
        PyObject x = py.getModule("kotlin_db_cbor_event");
        String type = "post";
        String text = content;
        x.callAttr("insert_cbor", type, text);

        passLogToGUI();
    }

    @Override
    public void setUserVisibleHint(boolean isVisibleToUser) {
        super.setUserVisibleHint(isVisibleToUser);
        try {
            if (isVisibleToUser) {
                passLogToGUI();
            }
        }
        catch (Exception e){
            ;
        }
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
        PyObject x = py.getModule("kotlin_db_cbor_event");
        String[][] y = x.callAttr("get_my_feed_events").toJava(String[][].class);

        FeedLog[] feed = new FeedLog[y.length];

        int post_name = 1, post_timestamp = 2, post_content = 3;
        int username_new = 1, username_old = 2, username_timestamp = 3;

        for(int i = 0; i < y.length; i++){
            if (y[i][0].equals("post")) {
                String name = y[i][post_name];
                String timestamp = y[i][post_timestamp];
                String content = y[i][post_content];
                FeedLog f = FeedLog.postLog(name, content, timestamp);
                feed[i]  = f;
            }
            else{
                String new_ = y[i][username_new];
                String old = y[i][username_old];
                String timestamp = y[i][username_timestamp];
                FeedLog f = FeedLog.usernameLog(old, new_, timestamp);
                feed[i]  = f;
            }
        }

        Collections.reverse(Arrays.asList(feed));

        mAdapter = new MyFeedAdapter(feed);
        recyclerView.setAdapter(mAdapter);

    }

        /*
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
         */


    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }
}
