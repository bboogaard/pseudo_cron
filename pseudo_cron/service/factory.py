from .service import CronService


class CronServiceFactory:

    @classmethod
    def create_for_middleware(cls):
        return CronService()
