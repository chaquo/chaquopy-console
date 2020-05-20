package com.chaquo.python.utils;

import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.chaquo.python.console.R;

public class MyFeedAdapter extends RecyclerView.Adapter<MyFeedAdapter.MyViewHolder> {
    private FeedLog[] mDataset;

    // Provide a reference to the views for each data item
    // Complex data items may need more than one view per item, and
    // you provide access to all the views for a data item in a view holder
    public static class MyViewHolder extends RecyclerView.ViewHolder {
        // each data item is just a string in this case
        //public TextView name;
        //public TextView content;
        //public TextView timestamp;
        public LinearLayout layout;
        public MyViewHolder(LinearLayout l) {
            super(l);
            layout = l;
            //l.getLayoutParams().height = 300;
        }
    }

    // Provide a suitable constructor (depends on the kind of dataset)
    public MyFeedAdapter(FeedLog[] myDataset) {
        mDataset = myDataset;
    }

    // Create new views (invoked by the layout manager)
    @Override
    public MyFeedAdapter.MyViewHolder onCreateViewHolder(ViewGroup parent,
                                                         int viewType) {
        // create a new view
        LinearLayout l = (LinearLayout)  LayoutInflater.from(parent.getContext())
                .inflate(R.layout.my_text_view, parent, false);

        //TextView v = (TextView) LayoutInflater.from(parent.getContext())
        //        .inflate(R.layout.my_text_view, parent, false);

        MyViewHolder vh = new MyViewHolder(l);
        return vh;
    }

    // Replace the contents of a view (invoked by the layout manager)
    @Override
    public void onBindViewHolder(MyViewHolder holder, int position) {
        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        //((TextView) holder.layout.findViewById(R.id.my_text_view_name)).setText(mDataset[position].log_name);
        ((TextView) holder.layout.findViewById(R.id.my_text_view_content)).setText(mDataset[position].log_content);
        ((TextView) holder.layout.findViewById(R.id.my_text_view_timestamp)).setText(mDataset[position].timestamp);
        //holder.textView.setText(mDataset[position]);

    }


    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mDataset.length;
    }
}

