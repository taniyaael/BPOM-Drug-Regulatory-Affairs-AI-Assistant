@echo off
title BPOM Drug Regulatory Affairs AI Assistant
echo ======================================================================
echo    BPOM DRUG REGULATORY AFFAIRS AI ASSISTANT
echo    Badan Pengawas Obat dan Makanan Republik Indonesia
echo ======================================================================
echo.
echo Membuka aplikasi di browser http://127.0.0.1:5000...
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:5000"
echo.
echo Menjalankan server aplikasi BPOM Regulatory Affairs...
"C:\Users\taniya.elizabeth\AppData\Local\Programs\Python\Python312\python.exe" app.py
pause
