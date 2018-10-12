In this small Windows application, you can place arbitrary window always on the top of your screen with just one click.

# OS Compatability
Please note that this application can only be executed on Windows system since I used the Win32 API to manipulate window properties (although the GUI tool I used (PyQt5) is supposed to be cross-platform). Therefore, this application is **not** suitable for users using OSX or Unix or any OS other than Windows.

# On the Backstage
I originally designed this application only for myself when I wanted to watch animation while doing other works. I first tried to find and download a ready-made application to place the animation window on the top layer (while I'm using the online streaming, it is impossible to ask media player for help), only found ill-functioning or paid applications. Therefore, I decided to create a new one by myself.

You may find the source file is called `OnTopNeo` and be curious about what's new in this application. In fact, its predecessor is written in wxPython at an early time, and it was rewritten in PyQt5 now because it's hard to change the application appearance in wxPython.

# How to Use
If you're using the 64-bit Windows 10 OS, then you may just download the binary executable, or you can execute this python file (a python 3.6 above interpreter and PyQt5 package required). If you find inconvenient using the interpreter, you can try to compile it with `pyinstaller` package.

After this application started up, just tick the box before the application title, then, enjoy it!

If you want to open a small window playing the animation at the corner of your screen just like me, I strongly recommend a Chrome extension [Separate Window](https://chrome.google.com/webstore/detail/separate-window/cbgkkbaghihhnaeabfcmmglhnfkfnpon) to collaborate with my application. The Separate Window can create a new explorer page contains only the media player, then you can resize it and place the page at wherever you want!
