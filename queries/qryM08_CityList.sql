SELECT
    CityID,
    CityName,
    Country,
    Province,
    Latitude,
    Longitude,
    Elevation,
    TimeZoneID,
    Enabled
FROM Cities
WHERE Enabled = 1
ORDER BY CityName;
