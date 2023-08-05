# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_click']

package_data = \
{'': ['*']}

install_requires = \
['click<8',
 'first>=2.0.2,<3.0.0',
 'pyee>=8.1.0,<9.0.0',
 'slack-bolt>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'slack-click',
    'version': '2.0.0',
    'description': 'Click support for Slack-Bolt apps',
    'long_description': '# Click support for Slack Apps\n\nAs a Python\n[Slack-Bolt](https://slack.dev/bolt-python/tutorial/getting-started)\napplication developer I want to create slash-command that are composed with the\nPython [Click](https://click.palletsprojects.com/) package.  I use the\n[FastAPI](https://fastapi.tiangolo.com/) web framework in asyncio mode.\n\nI need support for  `--help` `--version` and any usage error to be properly\nsent as Slack messages.\n\n# Quick Start\n\nCheck out the [example](example/README.md) application.\n\n# Async Usage\n\nThe following example illustrates how to device a Click group object and bind\nit to the Slack-Bolt command listener.  In this example the code is all\nasyncio.  Click was not written to support async io natively, so the\n@click_async decorator is required.\n\nBy default the Developer should pass the Slack-Bolt request instance as the\nClick obj value when executing the Click group/command.  There is a mechanism\nto change this behavior, shown in a later example.\n\n```python\nimport click\nfrom slack_bolt.request.async_request import AsyncBoltRequest as Request\nfrom slack_click.async_click import click_async, version_option, AsyncSlackClickGroup\n\n# -----------------------------------------------------------------------------\n# Define a Click group handler for the Slack Slash-Command\n#\n# Notes:\n#   @click_async decorator must be used for asyncio mode\n#   @click.pass_obj inserts the click.Context obj into the callback parameters\n#       By default the obj is the Slack-Bolt request instance; see the\n#       @app.command code further down.\n# -----------------------------------------------------------------------------\n\n@click.group(name="/clicker", cls=AsyncSlackClickGroup)\n@version_option(version="0.1.0")\n@click.pass_obj\n@click_async\nasync def cli_click_group(request: Request):\n    """\n    This is the Clicker /click command group\n    """\n    say = request.context["say"]\n    await say("`/click` command invoked without any commands or options.")\n\n\n# -----------------------------------------------------------------------------\n# Register the command with Slack-Bolt\n# -----------------------------------------------------------------------------\n\n@app.command(cli_click_group.name)\nasync def on_clicker(request: Request, ack, say):\n    await ack()\n    await say("Got it.")\n\n    return await cli_click_group(prog_name=cli_click_group.name, obj=request)\n\n# -----------------------------------------------------------------------------\n# Add a command the Click group\n# -----------------------------------------------------------------------------\n\n@cli_click_group.command("hello")\n@click.pass_obj\nasync def click_hello_command(request: Request):\n    await request.context.say(f"Hi there <@{request.context.user_id}> :eyes:")\n```\n\n## Identifying the Slack-Bolt Request\n\nAs a Developer you may need to pass the Click obj as something other than the\nbolt request direct, as shown in the example above.  You can identify\nwhere the Slack-Bolt request object can be found in the obj by passing\na callback function to the click.command() or click.group() function called\n`slack_request`.  This parameter expects a function that takes the click obj and\nreturns the slack request.\n\nThe example below uses an inline lambda to get the request from the obj as a\ndictionary, using a the key "here".\n\n```python\nfrom random import randrange\n\nimport click\nfrom slack_bolt.request.async_request import AsyncBoltRequest as Request\nfrom slack_click.async_click import click_async, AsyncSlackClickCommand\n\n# -----------------------------------------------------------------------------\n# /fuzzy command to manifest an anminal\n# -----------------------------------------------------------------------------\n\n\nanimals = [":smile_cat:", ":hear_no_evil:", ":unicorn_face:"]\n\n\n@click.command(\n    name="/fuzzy", cls=AsyncSlackClickCommand, slack_request=lambda obj: obj["here"]\n)\n@click_async\n@click.pass_obj\nasync def cli_fuzzy_command(obj: dict):\n    request = obj["here"]\n    say = request.context["say"]\n    this_animal = animals[randrange(len(animals))]\n\n    await say(f"Poof :magic_wand: {this_animal}")\n\n\n@app.command(cli_fuzzy_command.name)\nasync def on_fuzzy(request: Request, ack):\n    await ack()\n    return await cli_fuzzy_command(\n        prog_name=cli_fuzzy_command.name, obj={"here": request}\n    )\n```\n\n# Customizing Help\n\nIf you want to change the Slack message format for help or usage methods you can\nsubclass `AsyncSlackCLickCommand` or `AsyncSlackClickGroup` and overload the methods:\n\n* *slack_format_help* - returns the Slack message payload (dict) for `--help`\n* *slack_format_usage_help* - returns the Slack message payload (dict) when click exception `UsageError` is raised.\n\n\n# References\n* [Click - Docs Home](https://click.palletsprojects.com/)\n* [Getting Started with Slack Bolt](https://slack.dev/bolt-python/tutorial/getting-started)\n* [Slack-Bolt-Python Github](https://github.com/slackapi/bolt-python)\n* [Internals of Bolt Callback Parameters](https://github.com/slackapi/bolt-python/blob/main/slack_bolt/listener/async_internals.py)\n',
    'author': 'Jeremy Schulman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeremyschulman/slack-click',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
