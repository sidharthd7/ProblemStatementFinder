from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from collections import defaultdict
import time
from .config import settings
from .logging import logger

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.rate_limit = settings.RATE_LIMIT_PER_MINUTE
        self.window = 60 # 1 minute window
        
    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        current_time = time.time()
        
        # clean old req
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window
        ]
        
        # check if rate limit exceeded
        if len(self.requests[client_ip]) >= self.rate_limit:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Too many requests",
                    "retry_after": int(self.window - (current_time - self.requests[client_ip][0])),
                    "limit": self.rate_limit,
                    "window": self.window
                }
            )
            
        # add current req
        self.requests[client_ip].append(current_time)
        logger.debug(f"Request from IP {client_ip} processed. Current rate: {len(self.requests[client_ip])}/{self.rate_limit}")
        
        
rate_limiter = RateLimiter()