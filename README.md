# Chaquopy console app

This is an example of an interactive Python console script running in an Android app using
[Chaquopy](https://chaquo.com/chaquopy/). Some starting points:

* The example Python script is in 
  [`app/src/main/python/main.py`](https://github.com/chaquo/chaquopy-console/blob/master/app/src/main/python/main.py).
  You can replace this with your own code.
* The Android activity which hosts it is in 
  [`app/src/main/java/com/chaquo/python/console/MainActivity.java`](https://github.com/chaquo/chaquopy-console/blob/master/app/src/main/java/com/chaquo/python/console/MainActivity.java).
* The Chaquopy configuration (Python version, pip requirements list, etc.) is in 
  [`app/build.gradle`](https://github.com/chaquo/chaquopy-console/blob/master/app/build.gradle).
