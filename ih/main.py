from ih.app import settings
from ih.db.init_db import init_db
import uvicorn

def main():
    uvicorn.run(
        "ih.app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        #log_level=settings.LOG_LEVEL.lower(),
        #workers=1,
        reload=True,
        forwarded_allow_ips=settings.HOST_IP,
        #ssl_keyfile=settings.TLS_PRIVATE_KEY_PATH,
        #ssl_certfile=settings.TLS_CERTIFICATE_PATH,
        log_level=settings.LOG_LEVEL,
    )


if __name__ == "__main__":
    init_db()
    main()