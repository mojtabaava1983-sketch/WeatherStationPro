# M08 Final Form Specification

## frmMainNavigation
The main Access shell.

Buttons:
- Weather Dashboard
- City Manager
- Forecast
- Sunrise / Sunset
- Reports
- Exit

## frmWeatherDashboard
The primary presentation surface of WeatherStation Pro.

Header:
- application name;
- selected city;
- observation time;
- data source.

Current weather cards:
- Temperature
- Feels Like
- Humidity
- Pressure
- Wind Speed
- Wind Direction
- Gust
- Cloud Cover
- Visibility
- Dew Point
- Rain
- Snow
- Weather Code
- Data Quality

Actions:
- Refresh
- Change City
- Open Forecast
- Open Sunrise/Sunset

Presentation rule:
NULL values are shown as "—".
M08 never invents or calculates missing weather values.

## frmCityManager
Enabled-city administration:
- list;
- add;
- edit;
- enable/disable;
- geographic metadata.

Validation:
Latitude -90..90.
Longitude -180..180.

## frmForecast
Presentation only.
Forecast calculation belongs to M06.

## frmSunTimes
Presentation only.
Astronomical calculation belongs to M07.

## frmReports
Navigation to M09.

## Presentation Core resolution

All dashboard/presentation responsibilities that were previously described as
"Presentation Core" are represented here as M08 UI behavior. There is no
separate Presentation Core module in the official architecture.
