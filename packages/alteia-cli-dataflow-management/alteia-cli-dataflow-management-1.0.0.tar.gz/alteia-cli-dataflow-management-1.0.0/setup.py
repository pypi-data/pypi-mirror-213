# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alteia_cli', 'alteia_cli.plugins.dataflow_management']

package_data = \
{'': ['*']}

install_requires = \
['alteia-cli==1.3',
 'alteia>=2.5.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'types-cachetools>=5.2.1,<6.0.0',
 'types-python-dateutil>=2.8.19.2,<3.0.0.0',
 'types-pyyaml>=6.0.12,<7.0.0']

setup_kwargs = {
    'name': 'alteia-cli-dataflow-management',
    'version': '1.0.0',
    'description': 'Alteia CLI extension for dataflow management',
    'long_description': '# `alteia datastreams`\n\n**Usage**:\n\n```console\n$ alteia datastreams [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `aggregate-partial-results`: Aggregate a datastream outputs using its...\n* `complete`: Complete a datastream.\n* `create`: Create a datastream from a datastream...\n* `describe`: Describe datastream and its datastream...\n* `get`: Get datastream description in yaml format.\n* `list`: List datastreams.\n* `list-partial-aggregations`: List ongoing aggregation for a datastream.\n* `monitor-assets`: Monitor datastream assets monitored.\n* `trigger`: Trigger a datastream in order to...\n\n## `alteia datastreams aggregate-partial-results`\n\nAggregate a datastream outputs using its aggregation parameters.\n\n**Usage**:\n\n```console\n$ alteia datastreams aggregate-partial-results [OPTIONS] DATASTREAM_ID\n```\n\n**Arguments**:\n\n* `DATASTREAM_ID`: Datastream ID  [required]\n\n**Options**:\n\n* `--force-command / --no-force-command`: Force partial aggregation command even if another one is running.  [default: no-force-command]\n* `--help`: Show this message and exit.\n\n## `alteia datastreams complete`\n\nComplete a datastream.\n\n**Usage**:\n\n```console\n$ alteia datastreams complete [OPTIONS] DATASTREAM_ID\n```\n\n**Arguments**:\n\n* `DATASTREAM_ID`: Datastream ID  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `alteia datastreams create`\n\nCreate a datastream from a datastream template.\n\n**Usage**:\n\n```console\n$ alteia datastreams create [OPTIONS]\n```\n\n**Options**:\n\n* `--name TEXT`: Datastream name.  [required]\n* `--template TEXT`: Datastream Template identifier.  [required]\n* `--source TEXT`: Source url.  [required]\n* `--synchronisation TEXT`: Source synchronisation.  [default: automatic]\n* `--start-date TEXT`: Start date in format 2023-01-01T01:01:01Z.  [required]\n* `--end-date TEXT`: End date in format 2023-02-01T01:01:01Z.  [required]\n* `--description TEXT`: Description.\n* `--regex TEXT`: Regex.  [default: .*las$]\n* `--project TEXT`: Project identifier, used in order to describe a project target.\n* `--help`: Show this message and exit.\n\n## `alteia datastreams describe`\n\nDescribe datastream and its datastream files status.\n\n**Usage**:\n\n```console\n$ alteia datastreams describe [OPTIONS] DATASTREAM_ID\n```\n\n**Arguments**:\n\n* `DATASTREAM_ID`: Datastream ID  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `alteia datastreams get`\n\nGet datastream description in yaml format.\n\n**Usage**:\n\n```console\n$ alteia datastreams get [OPTIONS] DATASTREAM_ID\n```\n\n**Arguments**:\n\n* `DATASTREAM_ID`: Datastream ID  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `alteia datastreams list`\n\nList datastreams.\n\n**Usage**:\n\n```console\n$ alteia datastreams list [OPTIONS]\n```\n\n**Options**:\n\n* `--company TEXT`: Company ID.\n* `--limit INTEGER`: Limit number of results.  [default: 10]\n* `--asset-schema-repository TEXT`: Asset schema repository name.\n* `--asset-schema TEXT`: Asset schema name.\n* `--asset-schema-repository-id TEXT`: Asset schema repository id.\n* `--asset-schema-id TEXT`: Asset schema id.\n* `--help`: Show this message and exit.\n\n## `alteia datastreams list-partial-aggregations`\n\nList ongoing aggregation for a datastream.\n\n**Usage**:\n\n```console\n$ alteia datastreams list-partial-aggregations [OPTIONS] DATASTREAM_ID\n```\n\n**Arguments**:\n\n* `DATASTREAM_ID`: Datastream ID  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `alteia datastreams monitor-assets`\n\nMonitor datastream assets monitored.\n\n**Usage**:\n\n```console\n$ alteia datastreams monitor-assets [OPTIONS] DATASTREAM_ID\n```\n\n**Arguments**:\n\n* `DATASTREAM_ID`: Datastream ID  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `alteia datastreams trigger`\n\nTrigger a datastream in order to synchronise\nthe datastream files with its source.\n\n**Usage**:\n\n```console\n$ alteia datastreams trigger [OPTIONS] DATASTREAM_ID\n```\n\n**Arguments**:\n\n* `DATASTREAM_ID`: Datastream ID  [required]\n\n**Options**:\n\n* `--max-nb-files-sync INTEGER`: Maximum number of files to synchronize.  [default: 20]\n* `--fill-runnings-files / --no-fill-runnings-files`: Synchronize files in order to reach the maximum number of files.  [default: no-fill-runnings-files]\n* `--help`: Show this message and exit.\n\n# `alteia datastreamtemplates`\n\n**Usage**:\n\n```console\n$ alteia datastreamtemplates [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `create`: Create a datastream template.\n* `delete`: Delete a datastream template.\n* `list`: List datastream templates.\n\n## `alteia datastreamtemplates create`\n\nCreate a datastream template.\n\n**Usage**:\n\n```console\n$ alteia datastreamtemplates create [OPTIONS]\n```\n\n**Options**:\n\n* `--description PATH`: Path of the datastream template description (YAML file).  [required]\n* `--company TEXT`: Company identifier.  [required]\n* `--help`: Show this message and exit.\n\n## `alteia datastreamtemplates delete`\n\nDelete a datastream template.\n\n**Usage**:\n\n```console\n$ alteia datastreamtemplates delete [OPTIONS] DATASTREAMSTEMPLATE\n```\n\n**Arguments**:\n\n* `DATASTREAMSTEMPLATE`: Datastream template ID  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `alteia datastreamtemplates list`\n\nList datastream templates.\n\n**Usage**:\n\n```console\n$ alteia datastreamtemplates list [OPTIONS]\n```\n\n**Options**:\n\n* `--company TEXT`: Company ID.\n* `--limit INTEGER`: Limit number of results.  [default: 10]\n* `--asset-schema-repository TEXT`: Asset schema repository name.\n* `--asset-schema TEXT`: Asset schema name.\n* `--help`: Show this message and exit.\n',
    'author': 'Alteia Backend Team',
    'author_email': 'backend-team@alteia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
