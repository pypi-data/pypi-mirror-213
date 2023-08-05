from __future__ import annotations
import logging

from starlette.datastructures import URL
from starlette.routing import Router
from starlette.templating import pass_context

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, Any
from fastapi.templating import Jinja2Templates as FastAPIJinja2Templates

if TYPE_CHECKING:
    pass

class Jinja2Templates(FastAPIJinja2Templates):

    def _create_env(self, *args, **kwargs) -> "jinja2.Environment":
        from leanit_mweb import config
        cache_size = config.get("mweb", {}).get("templates", {}).get("cache_size", 1000)
        kwargs["cache_size"] = cache_size

        env = super()._create_env(*args, **kwargs)

        @pass_context
        def url(context: dict, name: str, **path_params: Any) -> URL:
            request = context["request"]
            router: Router = request.scope["router"]
            url_path = router.url_path_for(name, **path_params)
            return url_path

        env.globals["url"] = url
        return env