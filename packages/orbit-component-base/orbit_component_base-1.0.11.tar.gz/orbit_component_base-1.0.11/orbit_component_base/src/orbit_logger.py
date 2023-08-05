from loguru import logger as log


class OrbitLogger:

    def info(self, *args, **kwargs):
        log.success(args[0] % args[1:])

    def warning(self, *args, **kwargs):
        log.warning(args[0] % args[1:])

    def error(self, *args, **kwargs):
        log.error(args[0] % args[1:])
