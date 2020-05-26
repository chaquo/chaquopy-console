package com.chaquo.python.utils;

import android.graphics.Color;
import android.os.Build;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.RequiresApi;
import androidx.recyclerview.widget.RecyclerView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.console.R;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

public class PersonListAdapter extends RecyclerView.Adapter<PersonListAdapter.MyViewHolder> {
    private Person[] mDataset;

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
    public PersonListAdapter(Person[] myDataset) {
        mDataset = myDataset;
    }

    // Create new views (invoked by the layout manager)
    @Override
    public PersonListAdapter.MyViewHolder onCreateViewHolder(ViewGroup parent,
                                                             int viewType) {
        // create a new view
        LinearLayout l = (LinearLayout)  LayoutInflater.from(parent.getContext())
                .inflate(R.layout.friendslist_row, parent, false);

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
        final Person p = mDataset[position];

        final TextView t = holder.layout.findViewById(R.id.username);
        final LinearLayout row = holder.layout.findViewById(R.id.row);
        t.setText(p.name);
        if(p.trusted) {
            row.setBackgroundColor(Color.WHITE);
            t.setTextColor(Color.BLACK);

        }
        else{
            row.setBackgroundColor(Color.LTGRAY);
            t.setTextColor(Color.GRAY);
        }
        t.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
            @Override
            public void onClick(View view) {
                Python py = Python.getInstance();
                PyObject x = py.getModule("kotlin_db_cbor_event");
                if(p.trusted) {
                    Snackbar snackbar = Snackbar
                            .make(view, "You are now blocking " + p.name, Snackbar.LENGTH_LONG);
                    snackbar.show();
                    row.setBackgroundColor(Color.LTGRAY);
                    t.setTextColor(Color.GRAY);
                    x.callAttr("block","" + p.master_idx, "" + p.feed_id_idx);
                }
                else{
                    Snackbar snackbar = Snackbar
                            .make(view, "You are now trusting " + p.name, Snackbar.LENGTH_LONG);
                    snackbar.show();
                    row.setBackgroundColor(Color.WHITE);
                    t.setTextColor(Color.BLACK);
                    x.callAttr("trust","" + p.master_idx, "" + p.feed_id_idx);
                }
                p.trusted = !p.trusted;
            }
        });
        //holder.textView.setText(mDataset[position]);

    }


    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mDataset.length;
    }
}


