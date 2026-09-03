WeatherStation Pro - Product Integration Patch

Replaces src/main.py with an operational orchestrator connecting M01-M07, M09-M12 runtime services:
Database, Configuration, Weather API, Scheduler, Analysis, Forecast, Plugins, Reporting/CSV, Sunlight and Backup.

M08 Access: the uploaded project contains VBA/UI specifications but no .accdb/.mdb file, so the Access frontend cannot be embedded by this patch. It remains the Access presentation layer against the same SQLite database.

Build on Windows 10:
python -m PyInstaller --noconfirm --clean --onedir --name WeatherStationPro --paths src --add-data "src;src" --add-data "config;config" --add-data "database;database" --add-data "vba;vba" --add-data "ui;ui" --hidden-import sqlite3 --hidden-import _sqlite3 src\main.py
Copy weatherstation_runtime.db to dist\WeatherStationPro\
