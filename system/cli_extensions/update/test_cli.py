from click.testing import CliRunner
from ..cli.main import cli
from ..ai_core import AICore

def test_ai_command():
    core = AICore()
    runner = CliRunner()
    result = runner.invoke(cli, ['ai', '--model', 'deepseek'])
    assert 'AI Response' in result.output