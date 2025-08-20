from fastapi import FastAPI, HTTPException

from fastapi.responses import JSONResponse

from logger import logger

async def catch_exception_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as exc:
        logger.error(f"HTTP Exception: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    except Exception as exc:
        logger.error(f"Unhandled Exception: {str(exc)}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})