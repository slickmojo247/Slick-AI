from pathlib import Path
from ...commands import command, CommandResult, CommandResultLevel
from ...commands.decorators import command_logger

@command(
    name="file",
    help="File operations",
    usage="file <copy|move|delete> <source> [target]",
    aliases=["f"],
    category="file",
    min_args=2
)
@command_logger("file")
async def file_command(ctx, args: list) -> CommandResult:
    parser = ctx.command_parser
    subparsers = parser.add_subparsers(dest='operation', required=True)
    
    # Copy subcommand
    copy_parser = subparsers.add_parser('copy', help='Copy files')
    copy_parser.add_argument('source', help="Source path")
    copy_parser.add_argument('target', help="Target path")
    copy_parser.add_argument('--recursive', '-r', action='store_true')
    copy_parser.add_argument('--overwrite', action='store_true')
    
    # Move subcommand
    move_parser = subparsers.add_parser('move', help='Move files')
    move_parser.add_argument('source', help="Source path")
    move_parser.add_argument('target', help="Target path")
    
    # Delete subcommand
    delete_parser = subparsers.add_parser('delete', help='Delete files')
    delete_parser.add_argument('path', help="Path to delete")
    delete_parser.add_argument('--force', action='store_true')

    try:
        parsed = parser.parse_args(args)
    except Exception as e:
        return CommandResult(
            message=f"Invalid file command: {str(e)}",
            level=CommandResultLevel.ERROR,
            metadata={"example": "file copy source.txt target.txt"}
        )

    try:
        if parsed.operation == 'copy':
            result = file_copy(
                parsed.source,
                parsed.target,
                parsed.recursive,
                parsed.overwrite
            )
            return CommandResult(
                message=f"Copied {result['count']} items",
                data=result
            )
            
        elif parsed.operation == 'move':
            result = file_move(parsed.source, parsed.target)
            return CommandResult(
                message=f"Moved {parsed.source} to {parsed.target}",
                data=result
            )
            
        elif parsed.operation == 'delete':
            if not parsed.force and not confirm_deletion(parsed.path):
                return CommandResult(
                    message="Deletion cancelled",
                    level=CommandResultLevel.WARNING
                )
                
            result = file_delete(parsed.path)
            return CommandResult(
                message=f"Deleted {parsed.path}",
                data=result
            )
            
    except Exception as e:
        return CommandResult(
            message=f"File operation failed: {str(e)}",
            level=CommandResultLevel.ERROR,
            metadata={"operation": parsed.operation}
        )