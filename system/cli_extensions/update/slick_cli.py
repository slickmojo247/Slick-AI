#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = str(Path(__file__).parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from cli.commands import all_commands
import click

@click.group(commands=all_commands())
def slick():
    """SLICK AI Command Interface"""
    pass

if __name__ == '__main__':
    slick()