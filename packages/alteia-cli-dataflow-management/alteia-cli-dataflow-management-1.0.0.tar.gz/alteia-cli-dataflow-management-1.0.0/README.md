# `alteia datastreams`

**Usage**:

```console
$ alteia datastreams [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `aggregate-partial-results`: Aggregate a datastream outputs using its...
* `complete`: Complete a datastream.
* `create`: Create a datastream from a datastream...
* `describe`: Describe datastream and its datastream...
* `get`: Get datastream description in yaml format.
* `list`: List datastreams.
* `list-partial-aggregations`: List ongoing aggregation for a datastream.
* `monitor-assets`: Monitor datastream assets monitored.
* `trigger`: Trigger a datastream in order to...

## `alteia datastreams aggregate-partial-results`

Aggregate a datastream outputs using its aggregation parameters.

**Usage**:

```console
$ alteia datastreams aggregate-partial-results [OPTIONS] DATASTREAM_ID
```

**Arguments**:

* `DATASTREAM_ID`: Datastream ID  [required]

**Options**:

* `--force-command / --no-force-command`: Force partial aggregation command even if another one is running.  [default: no-force-command]
* `--help`: Show this message and exit.

## `alteia datastreams complete`

Complete a datastream.

**Usage**:

```console
$ alteia datastreams complete [OPTIONS] DATASTREAM_ID
```

**Arguments**:

* `DATASTREAM_ID`: Datastream ID  [required]

**Options**:

* `--help`: Show this message and exit.

## `alteia datastreams create`

Create a datastream from a datastream template.

**Usage**:

```console
$ alteia datastreams create [OPTIONS]
```

**Options**:

* `--name TEXT`: Datastream name.  [required]
* `--template TEXT`: Datastream Template identifier.  [required]
* `--source TEXT`: Source url.  [required]
* `--synchronisation TEXT`: Source synchronisation.  [default: automatic]
* `--start-date TEXT`: Start date in format 2023-01-01T01:01:01Z.  [required]
* `--end-date TEXT`: End date in format 2023-02-01T01:01:01Z.  [required]
* `--description TEXT`: Description.
* `--regex TEXT`: Regex.  [default: .*las$]
* `--project TEXT`: Project identifier, used in order to describe a project target.
* `--help`: Show this message and exit.

## `alteia datastreams describe`

Describe datastream and its datastream files status.

**Usage**:

```console
$ alteia datastreams describe [OPTIONS] DATASTREAM_ID
```

**Arguments**:

* `DATASTREAM_ID`: Datastream ID  [required]

**Options**:

* `--help`: Show this message and exit.

## `alteia datastreams get`

Get datastream description in yaml format.

**Usage**:

```console
$ alteia datastreams get [OPTIONS] DATASTREAM_ID
```

**Arguments**:

* `DATASTREAM_ID`: Datastream ID  [required]

**Options**:

* `--help`: Show this message and exit.

## `alteia datastreams list`

List datastreams.

**Usage**:

```console
$ alteia datastreams list [OPTIONS]
```

**Options**:

* `--company TEXT`: Company ID.
* `--limit INTEGER`: Limit number of results.  [default: 10]
* `--asset-schema-repository TEXT`: Asset schema repository name.
* `--asset-schema TEXT`: Asset schema name.
* `--asset-schema-repository-id TEXT`: Asset schema repository id.
* `--asset-schema-id TEXT`: Asset schema id.
* `--help`: Show this message and exit.

## `alteia datastreams list-partial-aggregations`

List ongoing aggregation for a datastream.

**Usage**:

```console
$ alteia datastreams list-partial-aggregations [OPTIONS] DATASTREAM_ID
```

**Arguments**:

* `DATASTREAM_ID`: Datastream ID  [required]

**Options**:

* `--help`: Show this message and exit.

## `alteia datastreams monitor-assets`

Monitor datastream assets monitored.

**Usage**:

```console
$ alteia datastreams monitor-assets [OPTIONS] DATASTREAM_ID
```

**Arguments**:

* `DATASTREAM_ID`: Datastream ID  [required]

**Options**:

* `--help`: Show this message and exit.

## `alteia datastreams trigger`

Trigger a datastream in order to synchronise
the datastream files with its source.

**Usage**:

```console
$ alteia datastreams trigger [OPTIONS] DATASTREAM_ID
```

**Arguments**:

* `DATASTREAM_ID`: Datastream ID  [required]

**Options**:

* `--max-nb-files-sync INTEGER`: Maximum number of files to synchronize.  [default: 20]
* `--fill-runnings-files / --no-fill-runnings-files`: Synchronize files in order to reach the maximum number of files.  [default: no-fill-runnings-files]
* `--help`: Show this message and exit.

# `alteia datastreamtemplates`

**Usage**:

```console
$ alteia datastreamtemplates [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a datastream template.
* `delete`: Delete a datastream template.
* `list`: List datastream templates.

## `alteia datastreamtemplates create`

Create a datastream template.

**Usage**:

```console
$ alteia datastreamtemplates create [OPTIONS]
```

**Options**:

* `--description PATH`: Path of the datastream template description (YAML file).  [required]
* `--company TEXT`: Company identifier.  [required]
* `--help`: Show this message and exit.

## `alteia datastreamtemplates delete`

Delete a datastream template.

**Usage**:

```console
$ alteia datastreamtemplates delete [OPTIONS] DATASTREAMSTEMPLATE
```

**Arguments**:

* `DATASTREAMSTEMPLATE`: Datastream template ID  [required]

**Options**:

* `--help`: Show this message and exit.

## `alteia datastreamtemplates list`

List datastream templates.

**Usage**:

```console
$ alteia datastreamtemplates list [OPTIONS]
```

**Options**:

* `--company TEXT`: Company ID.
* `--limit INTEGER`: Limit number of results.  [default: 10]
* `--asset-schema-repository TEXT`: Asset schema repository name.
* `--asset-schema TEXT`: Asset schema name.
* `--help`: Show this message and exit.
