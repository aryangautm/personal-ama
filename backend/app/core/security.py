from fastapi import Request
from slowapi import Limiter

from slowapi.util import get_remote_address
from app.core.config import settings


def get_real_ip(request: Request):
    if "x-forwarded-for" in request.headers:
        # Nginx/Proxy sets this.
        return request.headers["x-forwarded-for"].split(",")[0]
    else:
        # Fallback if not behind a proxy
        return get_remote_address(request)


limiter = Limiter(key_func=get_real_ip, default_limits=[settings.RATE_LIMIT])
