# ansible-fortimanager-generic

### What's the generic module?

The generic module is to fill the gap which exists between FortiManager features being published and Ansible modules reflecting those features.

### Setup the environment 
Make sure you have `ansible==2.8.0` installed with python2 or python3, then run the `setup.py` to copy the generic module to ansible module directory.

*ansible 2.9 and later have a problem with httpapi connection and is being fixed with ansible PR 62534*
```sh
$python3 setup.py 
$python2 setup.py # if you are using python2
```
This script also applies to Python virtual env.
### module usage

The generic module utilizes existing fortimanager plugin to encapsulate data to request FortiManager device. In specific, one request includes the following payload skeleton:

```
{
    "id": 1,
    "method": "...",
    "params": [ ... ],
    "session": "..."
}
```
With the generic fortimanager ansible module, the `id` and `session` are taken over by fortimanager httpapi plugin, users should ignore them, only `method` and `params` are user input. 

There are two ways to write an ansible playbook with the generic fortimananger module.

#### `json` with plain string

The `json` is defined as a string, user must provide the json-formatted string, one example of this sort is given as below: 
```
- hosts: fortimanager01
  connection: httpapi
  vars:
    adom: "root"
    ansible_httpapi_use_ssl: True
    ansible_httpapi_validate_certs: False
    ansible_httpapi_port: 443
  tasks:
    -   name: 'create a script on fortimanager'
        fmgr_generic:
             json: |
                  {
                   "method":"add",
                   "params":[
                    {
                         "url":"/dvmdb/adom/root/script",
                         "data":[
                            {
                               "name": "user_script0",
                               "type": "cli",
                               "desc": "The script is created by ansible",
                               "content": "the script content to be executed"
                            }
                          ]
                     }
                    ]
                  }
```

#### `method` and `params` with hierarchies
We also provide another way to write the ansible playbook which is less error-prone. Basically, a yaml-json conversion is done in playbook. In the module schema, only top-level parameters `method` and `params` are defined. 

The following example is written in `method` and `params` style:
```
- hosts: fortimanager01
  connection: httpapi
  vars:
    adom: "root"
    ansible_httpapi_use_ssl: True
    ansible_httpapi_validate_certs: False
    ansible_httpapi_port: 443
  tasks:
    -   name: 'create a script on fortimanager'
        fmgr_generic:
            method: "add"
            params:
                - url: "/dvmdb/adom/root/script"
                  data:
                    - name: "user_script0"
                      type: "cli"
                      desc: "The script is created by ansible"
                      content: "the script content to be executed"
```


__caveats: when all three parameters are given at the same time, `json` has higher priority over `method`&`params` to be chosen.__ 

To run the above examples , the ansible inventory must include the right fortimanager device and credentials:
```
$cat hosts
[myfortimanagers]
fortimanager01 ansible_host=fortimanager01_address ansible_user=APIUser ansible_password=Fortinet1!

[myfortimanagers:vars]
ansible_network_os=fortimanager

$ansible-playbook -i hosts script_add.yml
```
