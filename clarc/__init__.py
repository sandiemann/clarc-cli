__app_name__ = "clarc"
__version__ = "0.1.0"
__DB_NAME__ = "file::memory:?cache=shared"

(
    SUCCESS,
    DB_ERROR,
    OPERATIONAL_ERROR,
    FETCH_ERROR,
    STASH_ERROR,
) = range(5)

ERRORS = {
    DB_ERROR: "db connection error",
    FETCH_ERROR: "value fetch error",
    STASH_ERROR: "value stash error",
    OPERATIONAL_ERROR: "db operational error",
}