from ih.core.config import get_app_settings
from ih.db.init_db import init_db

from ih.core.logging.logging_config import LOGGING_CONFIG
import uvicorn

def main():

    settings = get_app_settings()
    uvicorn.run(
        "ih.app:app",
        host=settings.HOST,
        port=settings.PORT,
        #workers=1,
        reload=True,
        forwarded_allow_ips=settings.HOST_IP,
        #ssl_keyfile=settings.TLS_PRIVATE_KEY_PATH,
        #ssl_certfile=settings.TLS_CERTIFICATE_PATH,
        log_config=LOGGING_CONFIG,
    )


if __name__ == "__main__":
    main()