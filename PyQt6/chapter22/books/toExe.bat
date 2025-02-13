pyinstaller -w --upx-dir="C:\Users\Administrator\Desktop\upx-4.2.1-win64" ^
    --add-data="./res/book.dat:res" ^
    --add-data="./res/classification.dat:res" ^
    --add-data="./res/country.dat:res" ^
    --add-data="./res/book/BookCovers.png:book" ^
    LibraryManagement.py
    
    
REM C:\Users\Administrator\Desktop\upx-4.2.1-win64
REM 请换成自己的upx目录，不用也可以