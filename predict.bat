@echo off
cd /d "C:\detektor pemesanan penipuan"
if "%~1"=="" (
  echo Masukkan pesan setelah file ini.
  echo Contoh: predict.bat "Selamat Anda mendapatkan hadiah"
  pause
  exit /b 1
)
"C:\Users\raflu\AppData\Local\Programs\Python\Python313\python.exe" "src\detector.py" predict "%~1"
pause
