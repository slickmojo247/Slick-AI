import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from ...commands import command

class CommandResultLevel(Enum):
    SUCCESS = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()

@dataclass
class CommandResult:
    message: str
    level: CommandResultLevel = CommandResultLevel.SUCCESS
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

def command_logger(name: str):
    """Decorator to add consistent logging to command handlers"""
    def decorator(func):
        def wrapper(ctx, args: list, *args, **kwargs):
            logger = logging.getLogger(f'command.{name}')
            logger.info(f"Executing command with args: {args}")
            
            try:
                result = func(ctx, args, *args, **kwargs)
                if isinstance(result, CommandResult):
                    if result.level == CommandResultLevel.SUCCESS:
                        logger.info(f"Command succeeded: {result.message}")
                    elif result.level == CommandResultLevel.ERROR:
                        logger.error(f"Command failed: {result.message}")
                return result
            except Exception as e:
                logger.error(f"Command execution failed: {str(e)}", exc_info=True)
                return CommandResult(
                    message=f"Command failed: {str(e)}",
                    level=CommandResultLevel.ERROR
                )
        return wrapper
    return decorator

@command(
    name="template",
    help="Template for enhanced commands",
    usage="template <required> [--option VALUE]",
    aliases=["tpl"],
    category="system",
    min_args=1,
    max_args=3
)
@command_logger("template")
async def template_command(ctx, args: list) -> CommandResult:
    """
    Enhanced command template with:
    - Structured results
    - Consistent logging
    - Error handling
    - Progress tracking
    """
    parser = ctx.command_parser
    parser.add_argument('required', help="Required argument")
    parser.add_argument('--option', help="Optional parameter")
    parser.add_argument('--flag', action='store_true', help="Boolean flag")
    
    try:
        parsed = parser.parse_args(args)
    except Exception as e:
        return CommandResult(
            message=f"Invalid arguments: {str(e)}",
            level=CommandResultLevel.ERROR,
            metadata={"example": "template value --option test"}
        )
    
    try:
        # Command logic here
        if some_condition:
            return CommandResult(
                message="Operation completed successfully",
                data={"key": "value"},
                metadata={"stats": {"processed": 42}}
            )
        else:
            return CommandResult(
                message="Operation completed with warnings",
                level=CommandResultLevel.WARNING,
                metadata={"skipped_items": [...]}
            )
    except Exception as e:
        return CommandResult(
            message=f"Processing failed: {str(e)}",
            level=CommandResultLevel.ERROR,
            metadata={"failed_item": {...}}
        )