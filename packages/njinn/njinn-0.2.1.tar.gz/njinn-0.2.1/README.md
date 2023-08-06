# Njinn CLI & Client

## Installation

You can install the Njinn CLI from [PyPI](https://pypi.org/project/njinn/):

    pip install njinn

The client is supported on Python 3.7 and above.

## Njinn CLI Usage

- Pack install

  njinn pack install <repository_url>

Use --help to see available options and defaults.

## Njinn Client Usage

- The client allows interacting with Njinn via its REST API.
- To see available query string parameters, please refer to official Njinn Documentation.

### Summary

```python
api = NjinnAPI(host="https://njinn.io", token="*****")

# GET /workflows
api.workflows(limit=2)

# GET /workflows/1
api.workflows(1)

# POST /workflows
api.create(Workflow(title="Workflow 1"))

# PUT /workflows/1
api.workflows(1).save()

# DELETE /workflows/1
api.workflows(1).delete()
```

### Get execution state

```python
# GET /executions/1
execution = api.executions(1)
print(execution.state)
```

### Get running executions

```python
### GET /executions?workflow=1&state=RUNNING
executions = api.executions(workflow=1, state="RUNNING")
```

### Add a label to execution

```python
# Option 1:
# GET /executions/1
execution = api.executions(1)
execution.labels["my_label"] = "new"

# PATCH /executions/1 {...}
execution.save(fields="labels")

```

### Cancel execution

```python
# GET /executions/1
execution = api.executions(1)

# POST /executions/1/cancel {...}
execution.cancel()
```

### Run Workflow

```python
# GET /workflows/1
workflow= api.workflows(1)

# POST /workflows/1/run {...}
workflow.run()
```

### Create webhook

```python
# POST /hooks {...}
api.create(Webhook(name="W1", title="W1", workflow=1))
```

### Disable webhook

```python
# PUT /hooks/1 {...}
webhook = api.hooks(1)
webhook.is_active = False
webhook.save()
```

### Delete webhook

```python
# DELETE /hooks/1
api.webhooks(1).delete()
```

### Create config

```python
# POST /configs {...}
api.create(Config(name="W1", title="W1", values={"key1": "value1"}))
```

### Update config

```python
config = api.configs(1)
config.values["key1"] = "value1"

# PUT /configs {...}
config.save()
```

### Get execution log

```python
# GET /executions/1
execution = api.executions(1)

# GET /executions/1/log
print(execution.log())
```

### Get task result

```python
# GET /executions/1/tasks/task_1/result
result = api.executions(1).tasks("task_1").result()
print(result)
```
