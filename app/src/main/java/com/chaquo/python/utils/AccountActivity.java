package com.chaquo.python.utils;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Application;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.console.R;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.android.material.textfield.TextInputLayout;

import java.io.File;
import java.io.FilenameFilter;

public class AccountActivity extends BacNetActivity {

    public  String publicKey;
    public String privateKey;
    public String keyDirectory;
    private String fileExtension = ".key";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //Python py = Python.getInstance();
        //PyObject x = py.getModule("database.database.cbor_handler");
        //x.callAttr("test");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_account);
        keyDirectory = getBaseContext().getFilesDir().getPath();
        getAndSetPublicKey();
        setText();
        setName();

        FloatingActionButton button =  findViewById(R.id.floatingActionButton_updateUsername);
        button.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
            @Override
            public void onClick(View view) {
                updateUsername();
                Snackbar snackbar = Snackbar
                        .make(view, "Done!", Snackbar.LENGTH_LONG);
                snackbar.show();
            }
        });
    }

    public void setName(){
        Python py = Python.getInstance();
        PyObject x = py.getModule("main");
        String uname = x.callAttr("get_uname").toString();
        //TextView print_uname_text = findViewById(R.id.username_print);
        //print_uname_text.setText("Your username is " + uname);
    }

    //TODO
    public void updateUsername(){
        Python py = Python.getInstance();
        PyObject x = py.getModule("kotlin_db_cbor_event");
        TextInputLayout new_uname_field = findViewById(R.id.changeUsernameText);
        String new_uname = new_uname_field.getEditText().getText().toString();


        PyObject y = py.getModule("kotlin_db_cbor_event");
        String old = y.callAttr("get_uname").toString();
        if(new_uname.equals(old)){
            return;
        }
        if(new_uname.equals("")) {
            return;
        }

        x.callAttr("change_uname", new_uname);
        //System.out.println("hello from the other side");
        setName();
    }

    public class FileFilter implements FilenameFilter {

        private String fileExtension;

        public FileFilter(String fileExtension) {
            this.fileExtension = fileExtension;
        }

        @Override
        public boolean accept(File directory, String fileName) {
            return (fileName.endsWith(this.fileExtension));
        }
    }

    public void getAndSetPublicKey() {
        Python py = Python.getInstance();
        PyObject x = py.getModule("kotlin_db_cbor_event");
        String s = x.callAttr("gui_get_pk").toString();
        /* Sorry!
        FileFilter fileFilter = new FileFilter(fileExtension);
        File parentDir = new File(keyDirectory);
        // Put the names of all files ending with .txt in a String array
        String[] listOfTextFiles = parentDir.list(fileFilter);

        if (listOfTextFiles.length == 0) {
            System.out.println("No public key!");
            return;
        }
        String s = "";
        for (String file : listOfTextFiles) {
            //construct the absolute file paths...
            String absoluteFilePath = new StringBuffer(keyDirectory).append(File.separator).append(file).toString();
            s = s + file;
            System.out.println(absoluteFilePath);
        }

         */
        publicKey = s;
    }

    public void setText() {
        TextView keyInfos = findViewById(R.id.publicKey);
        keyInfos.setText(publicKey);
    }


    public static class Task extends DebugActivity.Task {
        public Task(Application app) {
            super(app);
        }

        @Override
        public void run() {
            py.getModule("main").callAttr("main");
        } //TODO
    }

    @Override
    protected Class<? extends Task> getTaskClass() {
        return Task.class;
    }
}
