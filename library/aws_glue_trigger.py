#!/usr/bin/python

# Copyright: (c) 2018, Ryo Manzoku (@rmanzoku)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.aws.core import AnsibleAWSModule
from ansible.module_utils.ec2 import camel_dict_to_snake_dict

# Non-ansible imports
import copy
try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass


def create_or_update_glue_trigger(client, module):
    changed = False
    return changed

def delete_glue_trigger(client, module):
    changed = False
    return changed

def main():

    argument_spec = (
        dict(
            state=dict(require=False, type='str', default='present',
                       choices=['present', 'absent']),
            name=dict(required=True, type='str'),
        )
    )

    module = AnsibleAWSModule(argument_spec=argument_spec
                              # required_if=[
                            #       ('state', 'present', ['role', 'command_script_location'])
                            # ]
    )

    client = module.client('glue')
    params = module.params

    if params.get('state') == 'present':
        changed = create_or_update_glue_trigger(client, params)
    else:
        changed = delete_glue_trigger(client, params)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
