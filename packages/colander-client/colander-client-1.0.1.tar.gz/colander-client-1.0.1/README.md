# Colander Python 3 client

Colander REST API python implementation.

Brings your project the ability to populate your [Colander](https://github.com/PiRogueToolSuite/colander) instance with interesting collected datas.

License: GPLv3

## Project status

* Case : Query
* Devices : Query / Create / Update
* PiRogueExperiment : Query / Create / Update
* Artifacts : Query / Create / Update

_Refer to Colander documentation for data type explanation._

## Usage example

### Instancing

```python
from colander_client.client import Client

base_url = 'https://my-colander-server'
api_key = 'my-user-api-key'

client = Client(base_url=base_url, api_key=api_key)
```

The library also support the following environment variables :
* `COLANDER_PYTHON_CLIENT_BASE_URL`
* `COLANDER_PYTHON_CLIENT_API_KEY`

Having such environment variables set, you can just do:

```python
from colander_client.client import Client

client = Client()
```

### Case management

Before all, you need a case to work with:

```python
# Assuming the given case id :
case_id = 'current-case-id-im-working-on'

case = client.get_case(case_id)
```

Your Case will be asked for each futur creation calls:

```python
artifact = client.upload_artifact(case=case, filepath='/tmp/dump', ...)
experiment = client.create_pirogue_experiment(case=case, pcap=pcap_artifact, ...)
```

Since, the Case is somehow the workspace you are working on during a Colander populating session,
you can use the following handy function:

```python
client.switch_case(case)
```

Then you may avoid mentioning case in futur creation calls:
```python
artifact = client.upload_artifact(filepath='/tmp/dump', ...)
experiment = client.create_pirogue_experiment(pcap=pcap_artifact, ...)
```

To disable case switching:
```python
client.switch_case(None)
```

In any state, Case presence at function call takes precedence.

### Artifact uploads

```python
a_type = client.get_artifact_type_by_short_name( 'SAMPLE' )
# Assuming we have switched to a Case
artifact = client.upload_artifact(
    filepath='/tmp/captured.file', artifact_type=a_type)
```

Large file upload progression can be followed with a progress callback:
```python
def progress(what, percent, status):
    print(f"{what} is at {percent}%, currently it is: {status}")
    # in case of artifact upload progress 'what' is the given filepath

a_type = client.get_artifact_type_by_short_name( 'SAMPLE' )
# Assuming we have switched to a Case
artifact = client.upload_artifact(
    filepath='/tmp/captured.file', artifact_type=a_type, progress_callback=progress)
```

When you have many uploads to proceed, you can globally set a callback on the client,
avoiding repetitively passing it at function calls:
```python
client.set_global_progress_callback(progress)
```

In any state, callback presence at function call takes precedence.

### PiRogue Experiment creation

```python
experiment = client.create_pirogue_experiment(
    name='My today investigation',
    pcap=pcap_artifact,
    socket_trace=socket_trace_artifact,
    sslkeylog=sslkeylog_artifact)
```

### Device creation

Device can be specified on Artifact or PiRogue Experiment.
The creation is as follow:
```python
d_type = client.get_device_type_by_short_name('LAPTOP')

pul_device = client.create_device(name='Potential unsecure laptop', device_type=d_type)
```

Then specified at Artifact or PiRogue Experiment creation:
```python
artifact = client.upload_artifact(
    filepath='/tmp/captured.file', artifact_type=a_type,
    extra_params={
        'extracted_from': pul_device
    })

experiment = client.create_pirogue_experiment(
    name='My today investigation',
    pcap=pcap_artifact,
    socket_trace=socket_trace_artifact,
    sslkeylog=sslkeylog_artifact,
    extra_params={
        'target_device': pul_device
    })
```