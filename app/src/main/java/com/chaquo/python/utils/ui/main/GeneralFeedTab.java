package com.chaquo.python.utils.ui.main;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.console.R;
import com.chaquo.python.utils.FeedLog;
import com.chaquo.python.utils.MyFeedAdapter;

public class GeneralFeedTab extends Fragment {
    private View v;
    private RecyclerView recyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;


    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        v = inflater.inflate(R.layout.my_feed_tab, container, false);
        recyclerView = v.findViewById(R.id.my_feed_recycle_tab);

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

        mAdapter = new MyFeedAdapter(feed);
        recyclerView.setAdapter(mAdapter);
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }
}
