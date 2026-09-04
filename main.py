from __future__ import annotations
import logging
import os
import sqlite3
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

FROZEN = getattr(sys, "frozen", False)
BASE_DIR = Path(sys.executable).resolve().parent if FROZEN else Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
if str(BASE_DIR) not in sys.path: sys.path.insert(0, str(BASE_DIR))
if str(SRC_DIR) not in sys.path: sys.path.insert(0, str(SRC_DIR))

from backup import BackupService
from config.application_settings import ApplicationSettings
from config.runtime_settings import RuntimeSettings
from data_analysis import DataAnalysisEngine, Observation
from database import WeatherRepository, WeatherService
from forecast import ForecastEngine, ForecastRequest
from plugins import PluginContext, PluginRegistry, load_plugin_factories
from reporting import ReportFilter, ReportingService, export_csv
from scheduler import Job, Schedule, Scheduler
from sunlight import SunlightEngine
from weather_api.client import HttpClient
from weather_api.engine import WeatherApiEngine
from weather_api.providers.open_meteo import OpenMeteoProvider

CITY_ID=1
SOURCE_ID=1
LAT=40.4093
LON=49.8671
DB=BASE_DIR/"weatherstation_runtime.db"
REPORTS=BASE_DIR/"reports"
BACKUPS=BASE_DIR/"backups"
LOGS=BASE_DIR/"logs"
M08_PATH=BASE_DIR/"WeatherStation_M08_Final.accdb"

def now(): return datetime.now(timezone.utc)
def ts(x): return int(x.timestamp())

def sql_rows(sql,params=()):
    with sqlite3.connect(DB) as c:
        c.row_factory=sqlite3.Row
        return [dict(r) for r in c.execute(sql,params).fetchall()]

def sql_insert(table,values):
    values={k:v for k,v in values.items() if v is not None}
    cols=list(values); marks=",".join("?" for _ in cols)
    q=",".join('"'+x+'"' for x in cols)
    with sqlite3.connect(DB) as c:
        cur=c.execute(f'INSERT OR IGNORE INTO "{table}" ({q}) VALUES ({marks})',[values[x] for x in cols]); c.commit(); return int(cur.lastrowid or 0)

def acquire(api,service):
    r=api.fetch({"latitude":LAT,"longitude":LON})
    v=r.observation.to_dict(); t=now(); observed=v.get("ObservedUTC") or t.isoformat()
    od=datetime.fromisoformat(observed.replace("Z","+00:00")) if isinstance(observed,str) else t
    v.update(CityID=CITY_ID,SourceID=SOURCE_ID,ObservationUTC=od.isoformat(),ObservationUnix=ts(od))
    rid=service.save_observation("WeatherCurrent",v)
    sql_insert("ImportStatus",{"CityID":CITY_ID,"SourceID":SOURCE_ID,"ImportUTC":t.isoformat(),"ImportUnix":ts(t),"Status":"success","HTTPStatus":r.status_code,"RecordsReceived":1,"RecordsSaved":1,"MissingFields":0,"DurationMS":0})
    sql_insert("ApiSources",{"SourceID":SOURCE_ID,"SourceName":"open-meteo","BaseURL":"https://api.open-meteo.com","ApiVersion":"v1","Priority":1,"Enabled":1,"LastUpdateUTC":t.isoformat(),"LastUpdateUnix":ts(t)})
    return rid,od

def analysis():
    rows=sql_rows('SELECT ObservationUTC,Temperature,Humidity,Pressure,WindSpeed,DataQuality FROM WeatherCurrent WHERE CityID=? ORDER BY ObservationUnix',(CITY_ID,))
    obs=[]
    for r in rows:
        try: dt=datetime.fromisoformat(r["ObservationUTC"].replace("Z","+00:00"))
        except Exception: continue
        obs.append(Observation(dt,{k:r[k] for k in ("Temperature","Humidity","Pressure","WindSpeed")},CITY_ID,SOURCE_ID,float(r.get("DataQuality") or 100)))
    return DataAnalysisEngine().summarize(obs,["Temperature","Humidity","Pressure","WindSpeed"]),obs

def make_forecast(obs):
    if len(obs)<3:return 0
    series=ForecastEngine(default_horizon_days=7,minimum_history=3).forecast(ForecastRequest(CITY_ID,"Temperature",7,24),[o.value("Temperature") for o in obs],last_observation_at=obs[-1].observed_at)
    t=now(); n=0
    for p in series.points:
        sql_insert("WeatherForecast",{"CityID":CITY_ID,"SourceID":SOURCE_ID,"ForecastRunUTC":t.isoformat(),"ForecastRunUnix":ts(t),"ForecastDateUTC":p.timestamp.isoformat(),"ForecastDateUnix":ts(p.timestamp),"MinTemperature":p.lower,"MaxTemperature":p.upper,"MorningTemperature":p.value,"NoonTemperature":p.value,"EveningTemperature":p.value,"NightTemperature":p.value,"DataQuality":p.confidence*100,"CreatedUTC":t.isoformat(),"CreatedUnix":ts(t)})
        n+=1
    return n

def make_sun():
    t=now(); n=0
    for s in SunlightEngine().calculate_range(date.today(),7,LAT,LON):
        sql_insert("SunData",{"CityID":CITY_ID,"SunDateUTC":s.date.isoformat(),"SunDateUnix":s.date.toordinal(),"SunriseUTC":s.sunrise_utc.isoformat() if s.sunrise_utc else None,"SunriseUnix":ts(s.sunrise_utc) if s.sunrise_utc else None,"SolarNoonUTC":s.solar_noon_utc.isoformat() if s.solar_noon_utc else None,"SolarNoonUnix":ts(s.solar_noon_utc) if s.solar_noon_utc else None,"SunsetUTC":s.sunset_utc.isoformat() if s.sunset_utc else None,"SunsetUnix":ts(s.sunset_utc) if s.sunset_utc else None,"CreatedUTC":t.isoformat(),"CreatedUnix":ts(t)})
        n+=1
    return n

def make_reports():
    REPORTS.mkdir(parents=True,exist_ok=True); svc=ReportingService(); total=0
    sets={
      "current_weather":sql_rows('SELECT C.CityName,W.* FROM WeatherCurrent W JOIN Cities C ON C.CityID=W.CityID WHERE C.Enabled=1 ORDER BY W.ObservationUnix DESC'),
      "weather_history":sql_rows('SELECT C.CityName,W.* FROM WeatherCurrent W JOIN Cities C ON C.CityID=W.CityID WHERE C.Enabled=1 ORDER BY W.ObservationUnix DESC'),
      "forecast":sql_rows('SELECT C.CityName,F.ForecastDateUTC AS ForecastUTC,F.MorningTemperature AS Temperature,F.RainProbability AS PrecipitationProbability,F.WeatherCode FROM WeatherForecast F JOIN Cities C ON C.CityID=F.CityID WHERE C.Enabled=1 ORDER BY F.ForecastDateUnix'),
      "sun_times":sql_rows('SELECT C.CityName,S.SunDateUTC AS Date,S.SunriseUTC AS Sunrise,S.SunsetUTC AS Sunset,S.SolarNoonUTC AS SolarNoon FROM SunData S JOIN Cities C ON C.CityID=S.CityID WHERE C.Enabled=1 ORDER BY S.SunDateUnix')}
    for rid,rows in sets.items():
        r=svc.build(rid,rows,ReportFilter(city_id=CITY_ID)); export_csv(REPORTS/f"{rid}.csv",r.columns,r.rows); total+=1
    return total

def cycle(api,service):
    rid,_=acquire(api,service); summary,obs=analysis(); fc=make_forecast(obs); sun=make_sun(); reports=make_reports(); b=BackupService(BACKUPS).create_backup(DB)
    return rid,summary,fc,sun,reports,b

def launch_m08():
    if not M08_PATH.exists():
        print("[WARN] M08 Access file not found:", M08_PATH)
        return False
    try:
        os.startfile(str(M08_PATH))
        print("[PASS] M08 Access launched")
        return True
    except Exception as exc:
        print("[WARN] M08 launch failed:", exc)
        return False

def main():
    LOGS.mkdir(parents=True,exist_ok=True); logging.basicConfig(filename=LOGS/"runtime.log",level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
    app=ApplicationSettings(); app.validate(); cfg=RuntimeSettings(); cfg.validate()
    if not DB.exists(): print(f"Database not found: {DB}"); return 1
    repo=WeatherRepository(DB); service=WeatherService(repo); api=WeatherApiEngine(OpenMeteoProvider(),HttpClient())
    registry=PluginRegistry(); registry.register_many(load_plugin_factories(["plugins.example_plugin"])); registry.initialize_all(PluginContext()); registry.start_all()
    scheduler=Scheduler(); state={}
    def job(): state["result"]=cycle(api,service); return state["result"][0]
    scheduler.add_job(Job("weatherstation_cycle",job,Schedule.seconds(cfg.acquisition_interval_seconds),run_immediately=True)); scheduler.start()
    print("="*48); print(" WEATHERSTATION PRO"); print(" OPERATIONAL RUNTIME"); print("="*48); print(f"Database: {DB}"); print(f"Reports: {REPORTS}"); print(f"Interval: {cfg.acquisition_interval_seconds}s")
    launch_m08()
    try:
        while True:
            for r in scheduler.tick():
                if r.success:
                    rid,s,fc,sun,reports,b=state["result"]; print(f"[PASS] cycle RecordID={rid} forecast={fc} sun={sun} reports={reports} backup={b.destination.name}")
                else: print(f"[FAIL] cycle {r.error}")
            time.sleep(.5)
    except KeyboardInterrupt: print("Shutdown requested")
    finally: scheduler.stop(); registry.stop_all(); registry.shutdown_all()
    return 0

if __name__=="__main__": raise SystemExit(main())
