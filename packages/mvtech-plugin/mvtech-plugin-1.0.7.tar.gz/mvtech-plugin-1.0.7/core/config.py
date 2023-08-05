import os
from loguru import logger
import sys
import logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s | %(message)s")

modelHeader = """
from pydantic import BaseModel
from typing import *

# 可自行修改增加校验精准度

"""
BASERUNPARAM = """
class BASE_RUN_PARAM(BaseModel):
    timeOut: int = None
"""
MODELTEMPLATE = """
class {{ className }}(BaseModel):
    {% if args %}
    {% for argName, argType in args %}
    {{ argName }}: {{ argType }}
    {% endfor %}
    {% else %}
    ...
    {% endif %}
"""

ACTIONTEMPLATE = """
from SDK.run_define import Actions
from SDK.base import *

from .models import {{ adapMdl }}, {{ inputModel }}, {{ outputModel }}, BASE_RUN_PARAM


class {{ actionsName }}(Actions):

    def __init__(self):
        # 初始化
        super().__init__()
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.baseRunModel = BASE_RUN_PARAM
        self.outputModel = {{ outputModel }}
        self.adapMdl = {{ adapMdl }}


    def adapter(self, data={}):
        # write your code
        ...    
    
    
    def run(self, params={}):
        # write your code
        ...

"""
TESTAPITEMPLATE = """
from actions import *
from fastapi import FastAPI,HTTPException
import os
import uvicorn
import typing
import json
from SDK.base import * 

desc = \
'''
  欢迎使用 1.0.0 版本SDK提供的FastAPI调试接口。\n
  
  Love it!  -- MVTECH

'''
test_server = FastAPI(title="MVTECH-Plugin Test Server", version="1.0.0", description=desc)
{% for name, className in init_list %}
@test_server.post("/actions/{{ name }}",response_model={{ className }}().outputModel,tags=["动作"])
def action_{{ name }}(action_name:str="{{ name }}",
                      adapter_data:{{ className }}().adapMdl=None,
                      baseRunModel:{{ className }}().baseRunModel=None,
                      input_data:{{ className }}().inputModel=None):
    
    clearLog()

    adapter_data = adapter_data.dict()

    baseRunModel = baseRunModel.dict()

    input_data = input_data.dict()

    output = {{ className }}()._run(input_data,adapter_data,baseRunModel)

    if output["body"].get("error_trace"):
        raise HTTPException(500,detail=output["body"]["error_trace"])
    else:
        output_data = output["body"]["output"]

    return output_data
{% endfor %}

  
def runserver():
    os.system("")
    log("attention","在浏览器内输入 http://127.0.0.1:7007/docs# 以进行接口测试")
    log("attention","在浏览器内输入 http://127.0.0.1:7007/redoc 以查看帮助文档")
    uvicorn.run(test_server,host="127.0.0.1", port=7007)

if __name__ == '__main__':

    runserver()
"""

TRIGGERSTEMPLATE = """
from SDK.run_define import Triggers
from SDK.base import *

from .models import {{ adapMdl }}, {{ inputModel }}, {{ outputModel }}


class {{ triggersName }}(Triggers):

    def __init__(self):
        # 初始化
        
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.adapMdl = {{ adapMdl }}


    def adapter(self, data={}):
        # write your code
        ...    

    def run(self, params={}):
        # write your code
        # 返回必须使用 self.send({})
        
        ...

"""

ACTIONSTESTTEMPLATE = """
{
	"version": "v1",
	"type": "action_start",
	"body": {
		"action": "{{ title }}",
		"meta": {},
		"adapter": {},
		"nextStep": null,
		"input_data": {}
	}
}

"""

TRIGGERSTESTTEMPLATE = """
{
	"version": "v1",
	"type": "trigger_start",
	"body": {
		"trigger": "{{ title }}",
		"meta": {},
		"adapter": {},
		"nextStep": {
			"send_url": "http://127.0.0.1:8001/send",
			"jwt": ""
		},
		"input_data": {}
      "enable_web": false
	}
}

"""

MAINTEMPLATE = """#!/usr/bin/env python

from SDK.plugin import Plugin
from SDK.cli import client

{% if actionClassees %}
import actions
{% endif %}
{% if triggerClassees %}
import triggers
{% endif %}
{% if indicatorReceiverClassees %}
import indicator_receivers
{% endif %}
{% if alarmReceiverClassees %}
import alarm_receivers
{% endif %}


# 整个程序入口


class {{ pluginName }}(Plugin):

    def __init__(self):
        super().__init__()
        
        {% for actionClass in actionClassees %}
        self.add_actions(actions.{{ actionClass }}())
        {% endfor %}

        {% for triggerClass in triggerClassees %}
        self.add_triggers(triggers.{{ triggerClass }}())
        {% endfor %}

        {% for indicatorReceiverClasse in indicatorReceiverClassees %}
        self.add_indicator_receivers(indicator_receivers.{{ indicatorReceiverClasse }}())
        {% endfor %}
        
        {% for alarmReceiverClasse in alarmReceiverClassees %}
        self.add_alarm_receivers(alarm_receivers.{{ alarmReceiverClasse }}())
        {% endfor %}


def main():

    client({{ pluginName }}())



if __name__ == '__main__':

    main()
    
"""

INITTEMPLATE = """
{% for name, className in init_list %}
from .{{ name }} import {{ className }}
{% endfor %}
"""

HELPTEMPLATE = """
# {{ name }}

## About
{{ name }}



## adapter

{% if adapter %}


{% for field_name, field_data in adapter.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|

{%- endfor %}


{% endif %}


## Actions

{% if actions %}

{% for action, actionData in actions.items() %}

### {{ action }}

---

{% for action_name,action_data in actionData.items() %}

{% if action_name == 'input' %}
#### Input

{% for field_name, field_data in action_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}

{% endif %}


{% if action_name == 'output' %}
#### Output

{% for field_name, field_data in action_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}


{% endif %}



{% endfor %}

{% endfor %}

{% endif %}



## Triggers

---

{% if triggers %}


{% for trigger, triggerData in triggers.items() %}

### {{ trigger }}

---

{% for trigger_name,trigger_data in triggerData.items() %}

{% if trigger_name == 'input' %}
#### Input

{% for field_name, field_data in trigger_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}

{% endif %}


{% if action_name == 'output' %}
#### Output

{% for field_name, field_data in action_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}


{% endif %}



{% endfor %}

{% endfor %}

{% endif %}


## Types

{% if types %}

{% for type_name, type_data in types.items() %}

### {{ type_name }}

{% for field_name, field_data in type_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|

{%- endfor %}

{% endfor %}

{% endif %}


## 版本信息
- {{ version }}

## 参考引用
"""

INDICATORRECEIVERSTEMPLATE = """
from SDK.run_define import IndicatorReceivers
from SDK.base import *

from .models import {{ adapMdl }}, {{ inputModel }}, {{ outputModel }}


class {{ indicator_receiversName }}(IndicatorReceivers):

    def __init__(self):
        # 初始化

        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.adapMdl = {{ adapMdl }}


    def adapter(self, data={}):
        # write your code
        ...    

    def run(self, params={}):
        # write your code
        # 返回必须使用 self.send({})

        ...

"""

INDICATORRECEIVERSTESTTEMPLATE = """
{
	"version": "v1",
	"type": "indicator_receiver_start",
	"body": {
		"receiver": "{{ title }}",
		"meta": {},
		"adapter": {},
		"nextStep": {
			"send_url": "http://127.0.0.1:8001/send",
			"jwt": ""
		},
		"input_data": {},
      "enable_web": false
	}
}

"""

INDICATORRECEIVERSMODELTYPES = """
class Indicator(BaseModel):
    uid: str
    type: str
    value: str
    source: str
    reputation: str
    threat_score: int
    rawed: str
    tagsed: Optional[str] = None
    status: Optional[bool] = None
    notes: Optional[str] = None
    casesed: Optional[str] = None
    created_at: str
    updated_at: str


class IndicatorDomain(BaseModel):
    uid: str
    indicator_uid: str
    primary_domain: Optional[str] = None
    admin_name: Optional[str] = None
    organization: Optional[str] = None
    admin_email: Optional[str] = None
    admin_phone: Optional[str] = None
    admin_address: Optional[str] = None
    register_at: Optional[str] = None
    renew_at: Optional[str] = None
    name_provider: Optional[str] = None
    name_servers: Optional[str] = None


class IndicatorUrl(BaseModel):
    uid: str
    indicator_uid: str
    hash: Optional[str] = None
    host: Optional[str] = None


class IndicatorIp(BaseModel):
    uid: str
    indicator_uid: str
    hostname: Optional[str] = None
    geo_country: Optional[str] = None
    geo_location: Optional[str] = None
    open_ports: Optional[str] = None


class IndicatorHash(BaseModel):
    uid: str
    indicator_uid: str
    sha256: Optional[str] = None
    sha1: Optional[str] = None
    md5: Optional[str] = None


class IndicatorEmail(BaseModel):
    uid: str
    indicator_uid: str
    primary_domain: Optional[str] = None


class IndicatorFile(BaseModel):
    uid: str
    indicator_uid: str
    filename: Optional[str] = None
    extension: Optional[str] = None
    size: Optional[str] = None
    sha256: Optional[str] = None
    sha1: Optional[str] = None
    md5: Optional[str] = None


class IndicatorHost(BaseModel):
    uid: str
    indicator_uid: str
    ip: Optional[str] = None
    mac: Optional[str] = None
    bios: Optional[str] = None
    memory: Optional[str] = None
    processors: Optional[str] = None
    os: Optional[str] = None


class IndicatorAccount(BaseModel):
    uid: str
    indicator_uid: str
    username: Optional[str] = None
    email: Optional[str] = None
    account_type: Optional[str] = None
    role: Optional[str] = None
    domain: Optional[str] = None
    organization: Optional[str] = None
"""

INDICATORRECEIVERSMODELTEMPLATE = """
class {{ className }}(BaseModel):

    indicator: Indicator
    indicator_sub: Union[IndicatorDomain, IndicatorUrl, IndicatorIp, IndicatorHash, IndicatorEmail, IndicatorFile, IndicatorHost, IndicatorAccount, None]

"""

ALARMRECEIVERSTEMPLATE = """
from SDK.run_define import AlarmReceivers
from SDK.base import *

from .models import {{ adapMdl }}, {{ inputModel }}, {{ outputModel }}


class {{ alarm_receiversName }}(AlarmReceivers):

    def __init__(self):
        # 初始化

        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.adapMdl = {{ adapMdl }}


    def adapter(self, data={}):
        # write your code
        ...    
from SDK.plugin
    def run(self, params={}):
        # write your code
        # 返回必须使用 self.send({})

        ...

"""

ALARMRECEIVERSTESTTEMPLATE = """
{
	"version": "v1",
	"type": "alarm_receiver_start",
	"body": {
		"alarm": "{{ title }}",
		"meta": {},
		"adapter": {},
		"nextStep": {
			"send_url": "http://127.0.0.1:8001/send",
			"jwt": ""
		},
		"input_data": {},
      "enable_web": false
	}
}

"""

ALARMRECEIVERSMODELTYPES = """
class Alarm(BaseModel):
    uid: str
    name: str
    alarm_ip: str
    sip: str
    tip: str
    source: str
    type: str
    reputation: str
    status: Optional[bool] = True
    raw: str
    created_at: str
    updated_at: str
    
"""

ALARMRECEIVERSMODELTEMPLATE = """
class {{ className }}(BaseModel):

    alarm: Alarm
    
"""
