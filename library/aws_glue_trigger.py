#!/usr/bin/python

# Copyright: (c) 2018, Ryo Manzoku (@rmanzoku)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.aws.core import AnsibleAWSModule
from ansible.module_utils.ec2 import camel_dict_to_snake_dict

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass


def _is_params_equal(user_params, current_params):
    return True


def _get_glue_trigger(client, name):
    try:
        return client.get_trigger(Name=name)['Trigger']
    except (BotoCoreError, ClientError) as e:
        if e.response['Error']['Code'] == 'EntityNotFoundException':
            return None
        else:
            raise e


def create_or_update_glue_trigger(client, params):

    user_params = dict()
    if _get_glue_trigger(client, params.get('name')) is None:
        # Create
        return True

    current_params = dict()
    if _is_params_equal(user_params, current_params):
        return False

    # Update
    return True


def delete_glue_trigger(client, params):
    changed = False
    return changed


def main():

    argument_spec = (
        dict(
            state=dict(require=False, type='str', default='present',
                       choices=['present', 'absent']),
            name=dict(required=True, type='str'),
            trigger_type=dict(required=True, type='str',
                              choice=['SCHEDULED', 'CONDITIONAL', 'ON_DEMAND']),
            schedule=dict(required=False, type='str'),
            actions=dict(required=True, type='list'),
        )
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('trigger_type', 'SCHEDULED', ['schedule'])
        ]
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
