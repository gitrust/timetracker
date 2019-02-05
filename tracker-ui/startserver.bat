@echo off

:: python httpd.py
python -m http.server --bind localhost --cgi 80
