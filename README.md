# ansible-fortimanager-generic

### What's the generic module?

The generic module is to fill the gap which exists between FortiManager features being published and Ansible modules reflecting those features.

**warning**: It's preferable to use [FortiManager Ansible Collection](https://galaxy.ansible.com/fortinet/fortimanager) instead unless some features are not available there.

### Setup the environment 
Make sure you have `ansible>=2.8.0` installed with python2 or python3, then run the `setup.py` to copy the generic module to ansible module directory.

*ansible core 2.9 and later must be patched prior to invoking playbook for the module*
```sh
$ python3 setup.py 
$ python2 setup.py # if you are using python2
$ source patch_ansible
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
                - url: "/dvmdb/adom/{{ adom }}/script"
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

### Customize error handling
This Ansible module is limited in handling errors for its nature of being generic, but we are still able to handle errors by overriding the failure conditions:
- `rc_succeeded` to override the status code to succeed.
- `rc_failed` to override the sttaus code to fail.
- Define ansible `failed_when` conditional statements.

One example is `/dvm/cmd/add/device`, 0 is returned if the device is not present and added successfully, -20010 is returned if the device already exists. other codes can be considered failure. we will present the examples one by one:

#### Detect failure using `failed_when` statement
```
- name: Test API
  hosts: fortimanager01
  gather_facts: no
  connection: httpapi
  collections:
    - fortinet.fortimanager
  vars:
    ansible_httpapi_use_ssl: True
    ansible_httpapi_validate_certs: False
    ansible_httpapi_port: 443
  tasks:
    - name: Provisioning
      fmgr_generic:
         method: exec
         params:
            -  url: /dvm/cmd/add/device
               data:
                  adom: root
                  device:
                     desc: Provisioned by ansible
                     device action: add_model
                     mgmt_mode: fmg
                     mr: 2
                     name: fortiVM01
                     os_type: fos
                     os_ver: '6.0'
                     sn: {{ sn }}
                  flags:
                    - none
      register: provision
      failed_when: provision.rc != 0 and provision.rc != -20010
```

#### Detect success using `rc_succeeded` statement
```
- name: Test API
  hosts: fortimanager01
  gather_facts: no
  connection: httpapi
  collections:
    - fortinet.fortimanager
  vars:
    ansible_httpapi_use_ssl: True
    ansible_httpapi_validate_certs: False
    ansible_httpapi_port: 443
  tasks:
    - name: Provisioning
      fmgr_generic:
         method: exec
         params:
            -  url: /dvm/cmd/add/device
               data:
                  adom: root
                  device:
                     desc: Provisioned by ansible
                     device action: add_model
                     mgmt_mode: fmg
                     mr: 2
                     name: fortiVM01
                     os_type: fos
                     os_ver: '6.0'
                     sn: {{ sn }}
                  flags:
                    - none
         rc_succeeded:
            - 0
            - -20010
```

#### Make failure using `rc_failed` statement intentionally

This is the case where a certain status code is considered failure.

```
- name: Test API
  hosts: fortimanager01
  gather_facts: no
  connection: httpapi
  collections:
    - fortinet.fortimanager
  vars:
    ansible_httpapi_use_ssl: True
    ansible_httpapi_validate_certs: False
    ansible_httpapi_port: 443
  tasks:
    - name: Provisioning
      fmgr_generic:
         method: exec
         params:
            -  url: /dvm/cmd/add/device
               data:
                  adom: root
                  device:
                     desc: Provisioned by ansible
                     device action: add_model
                     mgmt_mode: fmg
                     mr: 2
                     name: fortiVM01
                     os_type: fos
                     os_ver: '6.0'
                     sn: {{ sn }}
                  flags:
                    - none
         rc_failed:
            - 0
            - -20010
```

#### Priority of three statements

It's legal to define all three failure/success statements.

Among the three statements, `failed_when` is most privileged, `rc_failed` is less privileged and `rc_succeeded` is least privileged.

In the example below, the `failed_when` eventually takes effect to calculate the failure conditions.

```
    ... ... ..
        rc_succeeded:
            - 0
        rc_failed:
            - 0
    register: task
    failed_when:
        - task.rc != 0
```
