from gabgabgurus.config.api_config import APIVersions, api_config

open_api_url_v1 = api_config.get_open_api_url(api_version=APIVersions.V1.value)

SPECTACULAR_SETTINGS = {
    "TITLE": "gabgabgurus API",
    "DESCRIPTION": "API for gabgabgurus",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "SWAGGER_UI_SETTINGS": f"""{{
        deepLinking: true,
        urls: [
            {{url: "{open_api_url_v1}", name: "{APIVersions.V1.value}"}},
        ],
        presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
        layout: "StandaloneLayout",
        persistAuthorization: true,
        displayOperationId: true,
        filter: true
    }}""",
}
