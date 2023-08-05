import functools
from loguru import logger as log
from asyncio import sleep
from time import time
from os import times


async def run_and_log(func, args, kwargs):
    try:
        tstart = time()
        cstart = times()
        try:
            output = await func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
            return {'ok': False, 'error': str(e)}
        tend = time()
        cend = times()
        real_time = (tend - tstart) * 1000
        sys_time = (cend[0] - cstart[0]) * 1000
        usr_time = (cend[1] - cstart[1]) * 1000
        new_args = []
        for arg in args:
            if isinstance(arg, str):
                if len(arg) > 20:
                    arg = arg[:20] + '...'
            elif isinstance(arg, bytes):
                if len(arg) > 20:
                    arg = arg[:20] + b'...'
            new_args += [arg]
        if len(new_args) > 2:
            params = new_args[2]
            if isinstance(params, dict):
                log.log('RPC', f'{func.__name__} => {params.get("method")} :: real={real_time:.0f}ms, sys={sys_time:.0f}ms usr={usr_time:.0f}ms repeat@{1000/real_time:.0f}/sec')
                return output
        log.log('RPC', f'{func.__name__} :: real={real_time:.0f}ms, sys={sys_time:.0f}ms usr={usr_time:.0f}ms repeat@{1000/real_time:.0f}/sec') ## :: {new_args}')
        return output
    except Exception as e:
        log.exception(e)


def navGuard(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            retrying = False
            while True:
                try:
                    session = await args[0].get_session(args[1])
                except KeyError:
                    log.warning('<< disconnected dead session >>')
                    return {'ok': False, 'error': 'Server was restarted'}
                except Exception as e:
                    log.exception(e)
                    raise
                if not session.get('activated', False):
                    if not retrying:
                        log.debug(f'<< waiting for authentication >> {args[1]}')
                        retrying = True
                    await sleep(0.1)
                    continue
                return await run_and_log(func, args, kwargs)
        except Exception as e:
            log.exception(e)
    return wrapper


def apiSentry(permissions):
    def navGuard(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                retrying = False
                while True:
                    try:
                        session = await args[0].get_session(args[1])
                        if session.get('perm') not in permissions:
                            error = f'insufficient permissions, wanted: {permissions}, got: {session.get("perm")}'
                            log.error(error)
                            return { 'ok': False, 'error': error }
                    except KeyError:
                        log.warning('<< disconnected dead session >>')
                        return {'ok': False, 'error': 'Server was restarted'}
                    except Exception as e:
                        log.exception(e)
                        raise
                    if not session.get('activated', False):
                        if not retrying:
                            log.debug(f'<< waiting for authentication >> {args[1]}')
                            retrying = True
                        await sleep(0.1)
                        continue
                    return await run_and_log(func, args, kwargs)
            except Exception as e:
                log.exception(e)
        return wrapper
    return navGuard
