package com.chaquo.python.utils;

import android.graphics.Bitmap;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.chaquo.python.console.R;
import com.chaquo.python.utils.ui.main.Huffmann;

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
    public MyViewHolder onCreateViewHolder(ViewGroup parent,
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
        String content = mDataset[position].log_content;
        ((TextView) holder.layout.findViewById(R.id.my_text_view_timestamp)).setText(mDataset[position].timestamp);
        ((TextView) holder.layout.findViewById(R.id.my_text_view_name)).setText(mDataset[position].log_name);
        if(content.startsWith(BitmapManager.SEPARATOR)){
            int index = content.indexOf(BitmapManager.SEPARATOR, 1);
            String s = content.substring(index+1);
            //s = Huffmann.decode(s);
            Bitmap b = BitmapManager.fromStringToBitmap(s);
            ((ImageView) holder.layout.findViewById(R.id.img)).setImageBitmap(b);

            String newcon = content.substring(0,index).replace('|', ' ');
            ((TextView) holder.layout.findViewById(R.id.my_text_view_content)).setText(newcon);
        }
        else{
            //content = content.replace('|', ' ');
            ((TextView) holder.layout.findViewById(R.id.my_text_view_content)).setText(content);
        }
        //holder.textView.setText(mDataset[position]);

    }


    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mDataset.length;
    }
}

