Alvitr
======

Copyright (C) 2013 Takahiro Yoshimura <altakey@gmail.com>.  All rights reserved.

This is an experiment of tsearch2-based fulltext searching of Android SDK and beyond.


0. WHAT DOES IT LOOK LIKE?
--------------------------

     $ virtualenv ~/ve/alvitr
     ...
     $ source ~/ve/alvitr/bin/activate
     (alvitr)$ pip install beautifulsoup4 sqlalchemy
     ...
     (alvitr)$ ./index.sh /usr/local/android-sdk 18 # alternatively you can load corps/android-14.sql.xz (created from android-14 in SDK 21)
     ...
     (alvitr)$ python ./query.py
     usage: ./query.py [--limit=n] <keyword> ...
     (alvitr)$ python ./query.py --limit=8 android testing
     Searching [u'android', u'testing'] (limiting to 8)
     link:1:3.7:http://developer.android.com/tools/testing/testing_android.html
     link:1:2.4:http://developer.android.com/tools/testing/activity_test.html
     link:1:2.3:http://developer.android.com/tools/testing/activity_test.html
     link:1:2.3:http://developer.android.com/tools/testing/testing_otheride.html
     link:1:2.1:http://developer.android.com/tools/testing/testing_android.html
     link:1:1.8:http://developer.android.com/tools/testing/testing_otheride.html
     link:1:1.4:http://developer.android.com/tools/testing/testing_eclipse.html
     link:1:1.2:http://developer.android.com/tools/testing/testing_eclipse.html
     link:1:0.1:http://developer.android.com/sources/android-14/android/test/TestRunner.java
     link:1:0.1:http://developer.android.com/sources/android-14/com/android/server/am/ActivityManagerService.java
     link:1:0.0:http://developer.android.com/sources/android-14/android/test/mock/MockContentResolver.java
     link:1:0.0:http://developer.android.com/sources/android-14/com/android/server/PowerManagerService.java
     link:1:0.0:http://developer.android.com/sources/android-14/org/apache/harmony/security/tests/java/security/ProviderTest.java
     link:1:0.0:http://developer.android.com/sources/android-14/android/content/res/Resources.java
     link:1:0.0:http://developer.android.com/sources/android-14/android/view/WindowManager.java
     link:1:0.0:http://developer.android.com/sources/android-14/android/content/ContentResolver.java
     link:1:0.0:http://developer.android.com/samples/android-14/ApiDemos/tests/src/com/example/android/apis/app/ForwardingTest.java
     link:1:0.0:http://developer.android.com/samples/android-14/NotePad/src/com/example/android/notepad/NotePadProvider.java
     link:1:0.0:http://developer.android.com/samples/android-14/NotePad/tests/src/com/example/android/notepad/NotePadProviderTest.java
     link:1:0.0:http://developer.android.com/samples/android-14/ApiDemos/tests/src/com/example/android/apis/view/Focus2ActivityTest.java
     link:1:0.0:http://developer.android.com/samples/android-14/ApiDemos/res/values/strings.xml
     (alvitr)$

1. SEARCHING
-------------

Global (documentation, examples, source codes):

     (alvitr)$ python ./query.py --limit=8 android testing
     Searching [u'android', u'testing'] (limiting to 8)
     ...

Documentations only:

     (alvitr)$ python ./query.py --docs --limit=8 android testing
     Searching [u'android', u'testing'] (limiting to 8)
     link:1:3.7:http://developer.android.com/tools/testing/testing_android.html
     link:1:2.4:http://developer.android.com/tools/testing/activity_test.html
     link:1:2.3:http://developer.android.com/tools/testing/activity_test.html
     link:1:2.3:http://developer.android.com/tools/testing/testing_otheride.html
     link:1:2.1:http://developer.android.com/tools/testing/testing_android.html
     link:1:1.8:http://developer.android.com/tools/testing/testing_otheride.html
     link:1:1.4:http://developer.android.com/tools/testing/testing_eclipse.html
     link:1:1.2:http://developer.android.com/tools/testing/testing_eclipse.html

Examples only:

     (alvitr)$ python ./query.py --examples --limit=8 android testing
     Searching [u'android', u'testing'] (limiting to 8)
     link:1:0.0:http://developer.android.com/samples/android-14/ApiDemos/tests/src/com/example/android/apis/app/ForwardingTest.java
     link:1:0.0:http://developer.android.com/samples/android-14/NotePad/src/com/example/android/notepad/NotePadProvider.java
     link:1:0.0:http://developer.android.com/samples/android-14/NotePad/tests/src/com/example/android/notepad/NotePadProviderTest.java
     link:1:0.0:http://developer.android.com/samples/android-14/ApiDemos/tests/src/com/example/android/apis/view/Focus2ActivityTest.java
     link:1:0.0:http://developer.android.com/samples/android-14/ApiDemos/res/values/strings.xml

Source codes only:

     (alvitr)$ python ./query.py --sources --limit=8 android testing
     Searching [u'android', u'testing'] (limiting to 8)
     link:1:0.1:http://developer.android.com/sources/android-14/android/test/TestRunner.java
     link:1:0.1:http://developer.android.com/sources/android-14/com/android/server/am/ActivityManagerService.java
     link:1:0.0:http://developer.android.com/sources/android-14/android/test/mock/MockContentResolver.java
     link:1:0.0:http://developer.android.com/sources/android-14/com/android/server/PowerManagerService.java
     link:1:0.0:http://developer.android.com/sources/android-14/org/apache/harmony/security/tests/java/security/ProviderTest.java
     link:1:0.0:http://developer.android.com/sources/android-14/android/content/res/Resources.java
     link:1:0.0:http://developer.android.com/sources/android-14/android/view/WindowManager.java
     link:1:0.0:http://developer.android.com/sources/android-14/android/content/ContentResolver.java

2. INDEXING
-----------

     (alvitr)$ ./index.sh /usr/local/android-sdk 18
     ...


3. BUGS
--------

 * Insanely hackish.
 * Doesn't support languages other than English.
 * grep-mode doesn't like hyperlinks much.
 * Filename based matches tend to spam results.
 * Limit option works on per-domain basis only.
 * Documentation loader has to know Android Developers' HTML document DOM structure.
 * Has rather strict UTF-8 conformance requirement.
