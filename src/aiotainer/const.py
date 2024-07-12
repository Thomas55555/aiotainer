"""The constants for aiotainer."""

API_BASE_URL = "https://service.drum-darter.ts.net/api"
AUTH_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}
AUTH_HEADER_FMT = "Bearer {}"
EVENT_TYPES = [
    "status-event",
    "positions-event",
    "settings-event",
]
HUSQVARNA_URL = "https://developer.husqvarnagroup.cloud/"
REST_POLL_CYCLE = 300
WS_URL = "wss://ws.openapi.husqvarna.dev/v1"

