# logic/commands/command_decorators.py
import functools
import logging

def command_logger(name: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            logger = logging.getLogger(f'command.{name}')
            logger.info(f"Executing {name} with args: {args}")
            try:
                result = await func(ctx, *args, **kwargs)
                logger.info(f"Command {name} completed")
                return result
            except Exception as e:
                logger.error(f"Command {name} failed: {str(e)}", exc_info=True)
                raise
        return wrapper
    return decorator