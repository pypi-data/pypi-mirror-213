import io
import os
from pathlib import Path
from hashlib import sha256
from math import floor

from coreapi import Client as CoreApiClient
from coreapi.utils import File
from coreapi.auth import TokenAuthentication


class Client:
    _max_chunk_length_bytes = 1 * 1024 * 1024
    _client: CoreApiClient

    _base_url = None
    _api_url = None

    _current_case = None
    _global_progress_callback = None

    def __init__(self, base_url=None, api_key=None):

        if base_url is None:
            base_url = os.getenv("COLANDER_PYTHON_CLIENT_BASE_URL")

        if api_key is None:
            api_key = os.getenv("COLANDER_PYTHON_CLIENT_API_KEY")

        if base_url is None:
            raise Exception("No API base url provided (COLANDER_PYTHON_CLIENT_BASE_URL)")

        if api_key is None:
            raise Exception("No API Key provided (COLANDER_PYTHON_CLIENT_API_KEY)")

        self._base_url = base_url
        self._api_url = f"{self._base_url}/api"

        auth = TokenAuthentication(
            scheme='Token',
            token=api_key
        )

        self._client = CoreApiClient(auth=auth)
        self._root_document = self._client.get(f'{self._api_url}/schema', format='corejson')

    def _action(self, keys, params=None, validate=True, overrides=None,
                action=None, encoding=None, transform=None):
        return self._client.action(self._root_document, keys,
                                   params=params, validate=validate,
                                   overrides=overrides, action=action,
                                   encoding=encoding, transform=transform)

    @staticmethod
    def _no_progress(*args):
        pass

    @staticmethod
    def _unpack_ids_if_any(params):
        # WARNING: This assumes we will never have 'extra_params' items containing

        # Deep copy is unnecessary there since
        # potential modifications are only done at dict root level
        params = params.copy()
        for k, v in params.items():
            if isinstance(v,dict):
                if 'id' in v:
                    params[k] = v['id']
        return params

    def switch_case(self, case):
        self._current_case = case

    def set_global_progress_callback(self, progress_callback):
        self._global_progress_callback = progress_callback

    def get_case(self, case_id):
        return self._action(['cases', 'read'], {'id': case_id})

    def get_cases(self):
        return self._action(['cases', 'list'])

    def get_artifact_types(self):
        return self._action(['artifact_types', 'list'])

    def get_artifact_type_by_short_name(self, name):
        types = self.get_artifact_types()
        for t in types:
            if t['short_name'] == name:
                return t
        raise Exception(f"artifact type does not exist: {name}")

    def upload_artifact(self, filepath=None, case=None, artifact_type=None, progress_callback=None, extra_params=None):

        # Inputs assertion
        if self._current_case is None and case is None:
            raise Exception("No current case set (use switch_case or provide it at function call)")
        if filepath is None:
            raise Exception("No filepath provided")
        if artifact_type is None:
            raise Exception("No artifact type provided")

        # Sanitize inputs
        if case is None:
            case = self._current_case
        if extra_params is None:
            extra_params = dict()
        if progress_callback is None:
            if self._global_progress_callback is None:
                progress_callback = Client._no_progress
            else:
                progress_callback = self._global_progress_callback

        # Unpack ids if any
        extra_params = Client._unpack_ids_if_any(extra_params)

        # Gathering chunk hashes
        progress_callback(filepath, 0, 'hashing')

        path = Path(filepath)
        size = path.stat().st_size
        name = path.name
        chunks = {}

        with open(filepath, 'rb') as f:
            addr = 0
            buf = None
            # TODO: Clean
            # For debug purpose only
            # part = 0
            while buf != b'':
                buf = f.read(self._max_chunk_length_bytes)
                if len(buf) > 0:
                    digester = sha256()
                    digester.update(buf)
                    chunks[addr] = digester.hexdigest()
                    addr += len(buf)
                    # TODO: Clean
                    # For debug purpose only
                    # with open(f"/tmp/{name}.part.{part}", 'wb') as p:
                    #     p.write(buf)
                    # print(f"Written: /tmp/{name}.part.{part}")
                    # part += 1

        progress_callback(filepath, 0, 'hashed')

        upr = self._action(['upload_requests', 'create'], params={
            'name': path.name,
            'size': size,
            'chunks': chunks
        })

        progress_callback(filepath, 0, 'initiated')

        # Uploading chunks
        last_response = None
        with open(filepath, 'rb') as f:
            addr = 0
            buf = None
            while buf != b'':
                buf = f.read(self._max_chunk_length_bytes)
                if len(buf) > 0:
                    fpart = io.BytesIO(buf)

                    progress_callback(filepath, floor(100 * addr / size), 'uploading')

                    last_response = self._action(
                        ['upload_requests', 'partial_update'],
                        params={
                            'id': upr['id'],
                            'file': File(f"{addr}.{name}", fpart),
                            'addr': addr
                        },
                        encoding="multipart/form-data"
                    )

                    addr += len(buf)

        if last_response is None:
            if size > 0:
                progress_callback(filepath, 100, 'failed')
                raise Exception("Upload failed with no response but stuff to do")
        else:
            if not last_response['eof'] or not last_response['status'] == 'SUCCEEDED':
                progress_callback(filepath, 100, 'failed')
                raise Exception("Upload failed somehow")

        progress_callback(filepath, 100, 'complete')

        new_artifact = self._action(
            ['artifacts', 'create'],
            params={
                **{
                    'case': case['id'],
                    'type': artifact_type['id'],
                    'upload_request_ref': upr['id'],
                },
                **extra_params
            }
        )

        return new_artifact

    def create_pirogue_experiment(self, name=None, case=None, pcap=None, socket_trace=None, sslkeylog=None, extra_params=None):

        # Inputs assertion
        if name is None:
            raise Exception("No name provided")
        if self._current_case is None and case is None:
            raise Exception("No current case set (use switch_case or provide it at function call)")
        if pcap is None:
            raise Exception("No pcap artifact provided")
        if socket_trace is None:
            raise Exception("No socket trace artifact provided")
        if sslkeylog is None:
            raise Exception("No ssl key log artifact provided")

        # Sanitize inputs
        if case is None:
            case = self._current_case
        if extra_params is None:
            extra_params = dict()

        # Unpack ids if any
        extra_params = Client._unpack_ids_if_any(extra_params)

        return self._action(
            ['pirogue_experiments', 'create'],
            params={
                **{
                    'name': name,
                    'case': case['id'],
                    'pcap': pcap['id'],
                    'socket_trace': socket_trace['id'],
                    'sslkeylog': sslkeylog['id'],
                },
                **extra_params
            }
        )

    def get_device_types(self):
        return self._action(['device_types', 'list'])

    def get_device_type_by_short_name(self, short_name):
        dts = self.get_device_types()
        for t in dts:
            if t['short_name'] == short_name:
                return t
        raise Exception(f"device type does not exist: {short_name}")

    def get_device_by_id(self, device_id):
        return self._action(['devices', 'read'], {'id': device_id})

    def create_device(self, name=None, case=None, device_type=None, extra_params=None):
        if name is None:
            raise Exception("No name provided")
        if self._current_case is None and case is None:
            raise Exception("No current case set (use switch_case or provide it at function call)")
        if device_type is None:
            raise Exception("No device type provided")

        # Sanitize inputs
        if case is None:
            case = self._current_case
        if extra_params is None:
            extra_params = dict()

        # Unpack ids if any
        extra_params = Client._unpack_ids_if_any(extra_params)

        return self._action(
            ['devices', 'create'],
            params={
                **{
                    'name': name,
                    'case': case['id'],
                    'type': device_type['id'],
                },
                **extra_params
            }
        )