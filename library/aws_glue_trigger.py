#!/usr/bin/python
# encoding: utf-8

# Copyright: (c) 2018, Ryo Manzoku (@rmanzoku)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: aws_glue_trigger
short_description: Created glue trigger
description:
  - It depends on boto3

requirements:
  - "python >= 3"
  - boto3
"""

EXAMPLES = '''
- name: Delete
  aws_glue_trigger:
    state: absent
    name: gum

- name: Create
  aws_glue_trigger:
    state: present
    name: mch-prod-mch_core-gum
    trigger_type: SCHEDULED
    schedule: "cron(45 6 * * ? *)"
    actions:
      - job_name: mch-prod-mch_core-gum
'''

from ansible.module_utils.aws.core import AnsibleAWSModule


try:
    from botocore.exceptions import BotoCoreError, ClientError
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


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


def create_or_update_glue_trigger(client, params, module):

    user_params = dict()
    user_params['Name'] = params.get('name')
    user_params['Type'] = params.get('trigger_type')

    if user_params['Type'] == "SCHEDULED":
        user_params['Schedule'] = params.get('schedule')

    actions = [
        {'JobName': action.get('job_name')}
        for action in params.get('actions')
    ]

    user_params['Actions'] = actions

    if _get_glue_trigger(client, params.get('name')) is None:
        # Create
        try:
            client.create_trigger(**user_params)
        except (BotoCoreError, ClientError) as e:
            raise e
        return True
    else:
        try:
            del user_params['Type']
            client.update_trigger(
                Name=params.get('name'),
                TriggerUpdate=user_params
            )
        except (BotoCoreError, ClientError) as e:
            raise e
        return True


def delete_glue_trigger(client, params, module):

    if _get_glue_trigger(client, params.get('name')):
        try:
            client.delete_trigger(Name=params.get('name'))
            return True
        except (BotoCoreError, ClientError) as e:
            module.fail_json_aws(e)

    return False


def main():

    argument_spec = (
        dict(
            state=dict(require=False, type='str', default='present',
                       choices=['present', 'absent']),
            name=dict(required=True, type='str'),
            trigger_type=dict(required=False, type='str',
                              choice=['SCHEDULED', 'CONDITIONAL', 'ON_DEMAND']),
            schedule=dict(required=False, type='str'),
            actions=dict(required=False, type='list'),
        )
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('state', 'present', ['trigger_type', 'trigger_type', 'actions']),
            ('trigger_type', 'SCHEDULED', ['schedule'])
        ]
    )

    if not HAS_BOTO:
        module.fail_json(msg='boto3 required for this module, install via pip or your package manager')

    client = module.client('glue')
    params = module.params

    if params.get('state') == 'present':
        changed = create_or_update_glue_trigger(client, params, module)
    else:
        changed = delete_glue_trigger(client, params, module)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
