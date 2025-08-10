from pydantic_settings import BaseSettings
from typing            import Any, Dict

class APISettings(BaseSettings):
    """ Настройки для SwaggerUI, OpenAPI """

    debug             : bool = True
    docs_url          : str = "/docs"
    openapi_prefix    : str = ""
    openapi_url       : str = "/openapi.json"
    title             : str = "Example_three"
    description       : str = "Admin panel"
    version           : str = "0.1.0"
    main_router_prefix: str = "/api"

    def fastapi_kwargs(self) -> Dict[str, Any]:
        fastapi_kwargs: Dict[str, Any] = {
            "debug"         : self.debug,
            "docs_url"      : self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url"   : self.openapi_url,
            "title"         : self.title,
            "description"   : self.description,
            "version"       : self.version,
        }

        return fastapi_kwargs