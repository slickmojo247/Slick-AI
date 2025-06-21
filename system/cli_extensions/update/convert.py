import sys
from pathlib import Path
from ...commands import command, CommandResult, CommandResultLevel
from ...commands.decorators import command_logger
from systems.sync_core import SyncCore, FileConflictStrategy
from systems.platform_tools import get_platform_tools

@command(
    name="convert",
    help="Convert files between Windows and Linux formats",
    usage="convert <source> <target> --to <windows|linux> [--conflict <strategy>]",
    aliases=["cv"],
    category="file",
    min_args=2
)
@command_logger("convert")
async def convert_command(ctx, args: list) -> CommandResult:
    parser = ctx.command_parser
    parser.add_argument('source', help="Source file or directory path")
    parser.add_argument('target', help="Target file or directory path")
    parser.add_argument('--to', choices=['windows', 'linux'], required=True,
                      help="Target OS format")
    parser.add_argument('--conflict', choices=['source', 'target', 'newer', 'merge'],
                      default='newer', help="Conflict resolution strategy")
    parser.add_argument('--dry-run', action='store_true',
                      help="Show what would be converted without making changes")

    try:
        parsed = parser.parse_args(args)
    except Exception as e:
        return CommandResult(
            message=f"Invalid arguments: {str(e)}",
            level=CommandResultLevel.ERROR,
            metadata={"example": "convert src.txt dest.txt --to linux"}
        )

    converter = FileConverter()
    stats = {
        'converted': 0,
        'skipped': 0,
        'failed': 0,
        'target_os': parsed.to
    }

    try:
        if parsed.dry_run:
            result = converter.dry_run(parsed.source, parsed.target, parsed.to)
            return CommandResult(
                message=f"Dry run would convert {result['count']} files",
                level=CommandResultLevel.INFO,
                data=result
            )
        
        success = converter.convert(
            parsed.source,
            parsed.target,
            parsed.to,
            FileConflictStrategy[parsed.conflict.upper()]
        )
        
        if success:
            return CommandResult(
                message=f"Successfully converted to {parsed.to} format",
                data={"stats": converter.get_stats()}
            )
        else:
            return CommandResult(
                message="Conversion completed with errors",
                level=CommandResultLevel.WARNING,
                data={"stats": converter.get_stats()}
            )
    except Exception as e:
        return CommandResult(
            message=f"Conversion failed: {str(e)}",
            level=CommandResultLevel.ERROR,
            metadata={"stats": stats}
        )

class FileConverter:
    def __init__(self):
        self.sync = SyncCore()
        self.tools = get_platform_tools()
        self.stats = {
            'converted': 0,
            'skipped': 0,
            'failed': 0
        }

    def dry_run(self, source: str, target: str, target_os: str) -> dict:
        """Simulate conversion without actual changes"""
        source_path = Path(source)
        files = []
        
        if source_path.is_file():
            files.append(str(source_path))
        else:
            files = [str(f) for f in source_path.rglob('*') if f.is_file()]
        
        return {
            'count': len(files),
            'target_os': target_os,
            'sample_files': files[:5]  # Show first 5 as example
        }

    def convert(self, source: str, target: str, target_os: str, strategy: FileConflictStrategy) -> bool:
        """Execute actual conversion"""
        # ... (implementation from previous version)
        # Update self.stats during processing
        return self.stats['failed'] == 0

    def get_stats(self) -> dict:
        return self.stats.copy()