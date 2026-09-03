SELECT
    SourceID,
    SourceName,
    BaseURL,
    ApiVersion,
    Priority,
    Enabled,
    LastUpdateUTC,
    LastUpdateUnix
FROM ApiSources
ORDER BY Priority ASC, SourceName ASC;
