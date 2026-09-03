SELECT
    W.RecordID,
    W.CityID,
    C.CityName,
    C.Country,
    W.SourceID,
    W.ObservationUTC,
    W.ObservationUnix,
    W.Temperature,
    W.FeelsLike,
    W.Humidity,
    W.Pressure,
    W.WindSpeed,
    W.WindDirection,
    W.GustSpeed,
    W.CloudCover,
    W.Visibility,
    W.DewPoint,
    W.Rain,
    W.Snow,
    W.WeatherCode,
    W.DataQuality
FROM WeatherCurrent AS W
INNER JOIN Cities AS C
    ON W.CityID = C.CityID
INNER JOIN
(
    SELECT CityID, MAX(ObservationUnix) AS MaxObservationUnix
    FROM WeatherCurrent
    GROUP BY CityID
) AS L
    ON W.CityID = L.CityID
   AND W.ObservationUnix = L.MaxObservationUnix
WHERE C.Enabled = 1;
