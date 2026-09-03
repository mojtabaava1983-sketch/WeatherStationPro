PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA temp_store = MEMORY;
PRAGMA busy_timeout = 5000;

CREATE TABLE IF NOT EXISTS DatabaseInfo (
    DatabaseID INTEGER PRIMARY KEY CHECK (DatabaseID = 1),
    DatabaseVersion TEXT NOT NULL,
    SchemaVersion INTEGER NOT NULL,
    ApplicationVersion TEXT NOT NULL,
    CreatedUTC TEXT NOT NULL,
    CreatedUnix INTEGER NOT NULL,
    LastMigrationUTC TEXT,
    LastMigrationUnix INTEGER,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS Cities (
    CityID INTEGER PRIMARY KEY AUTOINCREMENT,
    CityName TEXT NOT NULL,
    Country TEXT NOT NULL,
    Province TEXT,
    Latitude REAL NOT NULL CHECK (Latitude BETWEEN -90 AND 90),
    Longitude REAL NOT NULL CHECK (Longitude BETWEEN -180 AND 180),
    Elevation REAL,
    TimeZoneID TEXT NOT NULL,
    Enabled INTEGER NOT NULL DEFAULT 1 CHECK (Enabled IN (0,1)),
    CreatedUTC TEXT NOT NULL,
    CreatedUnix INTEGER NOT NULL,
    UpdatedUTC TEXT,
    UpdatedUnix INTEGER,
    UNIQUE (CityName, Country, Latitude, Longitude)
);
CREATE INDEX IF NOT EXISTS IDX_City_Name ON Cities(CityName);
CREATE INDEX IF NOT EXISTS IDX_City_Country ON Cities(Country);

CREATE TABLE IF NOT EXISTS ApiSources (
    SourceID INTEGER PRIMARY KEY AUTOINCREMENT,
    SourceName TEXT NOT NULL,
    BaseURL TEXT NOT NULL,
    ApiVersion TEXT,
    Priority INTEGER NOT NULL DEFAULT 1 CHECK (Priority >= 1),
    Enabled INTEGER NOT NULL DEFAULT 1 CHECK (Enabled IN (0,1)),
    LastUpdateUTC TEXT,
    LastUpdateUnix INTEGER,
    UNIQUE (SourceName, BaseURL)
);

CREATE TABLE IF NOT EXISTS WeatherCurrent (
    RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
    CityID INTEGER NOT NULL,
    SourceID INTEGER NOT NULL,
    ObservationUTC TEXT NOT NULL,
    ObservationUnix INTEGER NOT NULL,
    Temperature REAL,
    FeelsLike REAL,
    Humidity REAL CHECK (Humidity IS NULL OR Humidity BETWEEN 0 AND 100),
    Pressure REAL,
    WindSpeed REAL,
    WindDirection REAL CHECK (WindDirection IS NULL OR (WindDirection >= 0 AND WindDirection <= 360)),
    GustSpeed REAL,
    CloudCover REAL CHECK (CloudCover IS NULL OR CloudCover BETWEEN 0 AND 100),
    Visibility REAL,
    DewPoint REAL,
    Rain REAL,
    Snow REAL,
    WeatherCode INTEGER,
    DataQuality REAL DEFAULT 100 CHECK (DataQuality IS NULL OR DataQuality BETWEEN 0 AND 100),
    CreatedUTC TEXT NOT NULL,
    CreatedUnix INTEGER NOT NULL,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID),
    FOREIGN KEY (SourceID) REFERENCES ApiSources(SourceID),
    UNIQUE (CityID, SourceID, ObservationUnix)
);
CREATE INDEX IF NOT EXISTS IDX_Current_CityTime ON WeatherCurrent(CityID, ObservationUnix);
CREATE INDEX IF NOT EXISTS IDX_Current_SourceTime ON WeatherCurrent(SourceID, ObservationUnix);


-- M01-Final-02 additions --

/* WeatherStation Pro | M01-Final-02
   Continuation of database/schema.sql
   Append after M01-Final-01.
*/

CREATE TABLE IF NOT EXISTS WeatherForecast (
    ForecastID INTEGER PRIMARY KEY AUTOINCREMENT,
    CityID INTEGER NOT NULL,
    SourceID INTEGER NOT NULL,
    ForecastRunUTC TEXT NOT NULL,
    ForecastRunUnix INTEGER NOT NULL,
    ForecastDateUTC TEXT NOT NULL,
    ForecastDateUnix INTEGER NOT NULL,
    MinTemperature REAL,
    MaxTemperature REAL,
    MorningTemperature REAL,
    NoonTemperature REAL,
    EveningTemperature REAL,
    NightTemperature REAL,
    Humidity REAL CHECK (Humidity IS NULL OR Humidity BETWEEN 0 AND 100),
    Pressure REAL,
    WindSpeed REAL,
    WindDirection REAL CHECK (WindDirection IS NULL OR (WindDirection >= 0 AND WindDirection <= 360)),
    GustSpeed REAL,
    RainProbability REAL CHECK (RainProbability IS NULL OR RainProbability BETWEEN 0 AND 100),
    RainAmount REAL,
    SnowAmount REAL,
    CloudCover REAL CHECK (CloudCover IS NULL OR CloudCover BETWEEN 0 AND 100),
    Visibility REAL,
    UVIndex REAL CHECK (UVIndex IS NULL OR UVIndex >= 0),
    WeatherCode INTEGER,
    DataQuality REAL CHECK (DataQuality IS NULL OR DataQuality BETWEEN 0 AND 100),
    CreatedUTC TEXT NOT NULL,
    CreatedUnix INTEGER NOT NULL,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID),
    FOREIGN KEY (SourceID) REFERENCES ApiSources(SourceID),
    UNIQUE (CityID, SourceID, ForecastRunUnix, ForecastDateUnix)
);
CREATE INDEX IF NOT EXISTS IDX_Forecast_CityDate
    ON WeatherForecast(CityID, ForecastDateUnix);
CREATE INDEX IF NOT EXISTS IDX_Forecast_Run
    ON WeatherForecast(ForecastRunUnix);

CREATE TABLE IF NOT EXISTS SunData (
    SunID INTEGER PRIMARY KEY AUTOINCREMENT,
    CityID INTEGER NOT NULL,
    SunDateUTC TEXT NOT NULL,
    SunDateUnix INTEGER NOT NULL,
    SunriseUTC TEXT,
    SunriseUnix INTEGER,
    SolarNoonUTC TEXT,
    SolarNoonUnix INTEGER,
    SunsetUTC TEXT,
    SunsetUnix INTEGER,
    DayLength INTEGER,
    CivilDawnUTC TEXT,
    CivilDawnUnix INTEGER,
    CivilDuskUTC TEXT,
    CivilDuskUnix INTEGER,
    NauticalDawnUTC TEXT,
    NauticalDawnUnix INTEGER,
    NauticalDuskUTC TEXT,
    NauticalDuskUnix INTEGER,
    AstronomicalDawnUTC TEXT,
    AstronomicalDawnUnix INTEGER,
    AstronomicalDuskUTC TEXT,
    AstronomicalDuskUnix INTEGER,
    CreatedUTC TEXT NOT NULL,
    CreatedUnix INTEGER NOT NULL,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID),
    UNIQUE (CityID, SunDateUnix)
);
CREATE INDEX IF NOT EXISTS IDX_Sun_CityDate ON SunData(CityID, SunDateUnix);

CREATE TABLE IF NOT EXISTS MoonData (
    MoonID INTEGER PRIMARY KEY AUTOINCREMENT,
    CityID INTEGER NOT NULL,
    MoonDateUTC TEXT NOT NULL,
    MoonDateUnix INTEGER NOT NULL,
    MoonRiseUTC TEXT,
    MoonRiseUnix INTEGER,
    MoonSetUTC TEXT,
    MoonSetUnix INTEGER,
    MoonPhase TEXT,
    MoonIllumination REAL CHECK (MoonIllumination IS NULL OR MoonIllumination BETWEEN 0 AND 100),
    CreatedUTC TEXT NOT NULL,
    CreatedUnix INTEGER NOT NULL,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID),
    UNIQUE (CityID, MoonDateUnix)
);
CREATE INDEX IF NOT EXISTS IDX_Moon_CityDate ON MoonData(CityID, MoonDateUnix);

CREATE TABLE IF NOT EXISTS AirQuality (
    AQID INTEGER PRIMARY KEY AUTOINCREMENT,
    CityID INTEGER NOT NULL,
    ObservationUTC TEXT NOT NULL,
    ObservationUnix INTEGER NOT NULL,
    AQI INTEGER CHECK (AQI IS NULL OR AQI >= 0),
    PM10 REAL CHECK (PM10 IS NULL OR PM10 >= 0),
    PM25 REAL CHECK (PM25 IS NULL OR PM25 >= 0),
    CO REAL CHECK (CO IS NULL OR CO >= 0),
    NO2 REAL CHECK (NO2 IS NULL OR NO2 >= 0),
    SO2 REAL CHECK (SO2 IS NULL OR SO2 >= 0),
    O3 REAL CHECK (O3 IS NULL OR O3 >= 0),
    NH3 REAL CHECK (NH3 IS NULL OR NH3 >= 0),
    DataQuality REAL CHECK (DataQuality IS NULL OR DataQuality BETWEEN 0 AND 100),
    CreatedUTC TEXT NOT NULL,
    CreatedUnix INTEGER NOT NULL,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID),
    UNIQUE (CityID, ObservationUnix)
);
CREATE INDEX IF NOT EXISTS IDX_AQI_CityTime ON AirQuality(CityID, ObservationUnix);

CREATE TABLE IF NOT EXISTS Settings (
    SettingKey TEXT PRIMARY KEY,
    SettingValue TEXT,
    ValueType TEXT NOT NULL DEFAULT 'string',
    Category TEXT,
    DefaultValue TEXT,
    Description TEXT,
    Editable INTEGER NOT NULL DEFAULT 1 CHECK (Editable IN (0,1)),
    UpdatedUTC TEXT,
    UpdatedUnix INTEGER
);

CREATE TABLE IF NOT EXISTS ImportStatus (
    ImportID INTEGER PRIMARY KEY AUTOINCREMENT,
    CityID INTEGER,
    SourceID INTEGER,
    ImportUTC TEXT NOT NULL,
    ImportUnix INTEGER NOT NULL,
    Status TEXT NOT NULL,
    HTTPStatus INTEGER,
    RecordsReceived INTEGER DEFAULT 0,
    RecordsSaved INTEGER DEFAULT 0,
    MissingFields INTEGER DEFAULT 0,
    ErrorMessage TEXT,
    DurationMS INTEGER,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID),
    FOREIGN KEY (SourceID) REFERENCES ApiSources(SourceID)
);
CREATE INDEX IF NOT EXISTS IDX_Import_CityTime ON ImportStatus(CityID, ImportUnix);
