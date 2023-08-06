import consul
import os
import json
import time
from functools import wraps
import boto3
from botocore.client import Config
import base64

mute = False
env = {'proto': None, 'values': {}}
runstep = {'current': {}, 'next': {}}
calls = []
current_call_limit = 0
next_call_limit = 0
stdio = {'out': [], 'error': []}
task_id = ''

c = consul.Consul(host=os.getenv('CONSUL_HOST') or 'consul-b2c-dev01.shein.com',
                  port=os.getenv('CONSUL_PORT') or '8500')

basic_conf = {
    'endpoint_url': os.getenv('BASE_URL') or 'http://s3-dev-test.test.paas-test.sheincorp.cn/',
    'aws_access_key_id': os.getenv('ACCESS_KEY_ID') or 'hello',
    'aws_secret_access_key': os.getenv('ACCESS_SECRET_ID') or 'testshein'
}
bucket = 'sotest-cloud-file'


def init(_mute, _env, _runstep, _task_id):
    global mute
    mute = _mute
    global env
    env = _env
    global runstep
    runstep = _runstep
    global task_id
    task_id = _task_id
    global calls
    calls = []
    global current_call_limit
    current_call_limit = 0
    global next_call_limit
    next_call_limit = 0
    global stdio
    stdio = {'out': [], 'error': []}


def get_state():
    return {'env': env, 'calls': calls, 'stdio': stdio}


def check(assertion, msg):
    calls.append({'method': 'check', 'args': [bool(assertion), msg]})


def stdio_write_out(s):
    stdio['out'].append(str(s))


def stdio_write_error(s):
    stdio['error'].append((str(s)))


def context_set_value(k, v, root=False):
    if not mute:
        raise Exception('You could only call setValue on an mute fn!')
    if not root:
        env['values'][k] = v
    else:
        node = env
        while bool(node['proto']):
            node = node['proto']
        node['values'][k] = v


def context_get_value(k):
    node = env
    while bool(node['proto']):
        if k in node['values']:
            return node['values'][k]
        node = node['proto']
    return None


def mutex(key='', ttl=30):
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            key_prefix = f'sotest_function_python_{task_id}'
            key_full = f'{key_prefix}_{key}' if key else key_prefix
            value = c.kv.get(key_full)[1]
            if value and value.get('Value'):
                return json.loads(value['Value'])
            session_id = c.session.create(lock_delay=0,
                                          name='sotest-utils-python',
                                          ttl=ttl,
                                          behavior='delete')
            set_result = c.kv.put(key=key_full,
                                  value=None,
                                  acquire=session_id)
            if set_result:
                fn_result = func(*args)
                set_result2 = c.kv.put(key=key_full,
                                       value=json.dumps(fn_result),
                                       acquire=session_id)
                if set_result2:
                    return fn_result
            time.sleep(1)
            return wrapper(*args)

        return wrapper

    return decorator


def create_cloud_file(filename, content, content_type='text/plain', is_base64=False):
    s3_client = boto3.client('s3',
                             **basic_conf,
                             api_version='2006-03-01',
                             use_ssl=False,
                             config=Config(s3={'addressing_style': 'path'}))
    buffer = content
    if is_base64:
        buffer = base64.b64decode(content).decode()
    localtime = time.localtime(time.time())
    final_key = f'{localtime.tm_year}/{localtime.tm_mon}/{localtime.tm_mday}/{int(time.time() * 1000)}/{filename}'
    store_path = basic_conf['endpoint_url'] + bucket + '/' + final_key

    res = s3_client.put_object(Body=buffer,
                               Bucket=bucket,
                               Key=final_key,
                               ContentType=content_type)
    return store_path


def check_equal(a, b, msg):
    calls.extend(['checkEqual', [a, b, msg]])


def check_lt(a, b, msg):
    calls.extend(['checkLt', [a, b, msg]])


def check_gt(a, b, msg):
    calls.extend((['checkGt', [a, b, msg]]))


def sotest_function_standard(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def sotest_function_authorization(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def sotest_function_verify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
