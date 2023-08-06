import os,json
from behave import given, when, then # pylint: disable=no-name-in-module (https://github.com/behave/behave/issues/641)
from behave_pandas import table_to_dataframe, dataframe_to_table
from pathlib import Path
from omnata_plugin_runtime.configuration import OutboundSyncConfigurationParameters
from omnata_plugin_runtime.omnata_plugin import ApiLimits, OutboundSyncRequest
import pandas
import unittest
from types import ModuleType
from snowflake.snowpark.functions import row_number, col, when_matched, when_not_matched, lit, current_timestamp, iff
import vcr
from pandas.testing import assert_frame_equal
import logging
import sys
import importlib
case = unittest.TestCase()

@given('the following records')
def step_impl_records(context):
    column_names = []
    row_strings = []
    column_bindings = []
    print(f"context.table: {context.table}")
    print(f"context.table.headings: {context.table.headings}")
    context.source_records = table_to_dataframe(context.table)

    print(f"source dataframe: {context.source_records}")


@when('we apply the records to the app with configuration parameters')
def step_impl_apply_records(context):
    if context.plugin_class is None:
        raise ValueError('You must define which plugin class and module is to be used ("we use the x class from the y module")')
    strategy=None
    connection_parameters = {}
    connection_secrets = {}
    sync_parameters = {}
    api_limits = {}
    field_mappings = []
    connection_method = None

    for row in context.table:
        if row['Property']=='strategy':
            strategy = json.loads(row['Value'])
        elif row['Property']=='connection_method':
            connection_method = row['Value']
        elif row['Property']=='connection_parameters':
            connection_parameters = json.loads(row['Value'])
        elif row['Property']=='api_limits':
            api_limits = json.loads(row['Value'])
        elif row['Property']=='connection_secrets':
            connection_secrets = json.loads(row['Value'])
        elif row['Property']=='sync_parameters':
            sync_parameters = json.loads(row['Value'])
        elif row['Property']=='field_mappings':
            field_mappings = json.loads(row['Value'])
        else:
            raise ValueError(f"Unknown apply parameter {row['Property']}")
    
    parameters = OutboundSyncConfigurationParameters.parse_obj({
        "sync_strategy": strategy,
        "connection_method": connection_method,
        "connection_parameters": connection_parameters,
        "connection_secrets": connection_secrets,
        "sync_parameters": sync_parameters,
        "field_mappings": field_mappings
    })
    # With API Limits, we remove rate limits to remove needless waiting
    # TODO: override concurrency setting due to pyvcr's thread non-safety
    context.plugin_instance = context.plugin_class()
    outbound_sync_request = OutboundSyncRequest(sync_id=0,
                                        sync_slug='',
                                        sync_branch_name='',
                                        sync_branch_id=None,
                                        connection_id=None,
                                        run_id=0,
                                        session=None,
                                        plugin_instance=context.plugin_instance,
                                        api_limits=[], # when running tests, since we're replaying HTTP we don't constrain
                                        rate_limit_state={},
                                        run_deadline=None,
                                        development_mode=True)
    outbound_sync_request._prebaked_record_state = context.source_records
    context.error = None
    try:
        context.apply_result = context.plugin_instance.sync_outbound(parameters,outbound_sync_request)
        # when using a managed_outbound_processing decorator, the results aren't returned from sync_outbound
        if context.apply_result is None:
            context.apply_result = outbound_sync_request.get_queued_results()
    except Exception as e:
        context.error = e
        logging.exception(e)

def load_script_from_file(app_name,action_name):
    f = open(os.path.join('scripts',app_name,f"{action_name}.py"))
    script_contents=f.read()
    mod = ModuleType('whatever.py','')
    exec(script_contents, mod.__dict__)
    return mod      

@given('we use the {plugin_class} class from the {plugin_module} module')
def step_impl_use_plugin_class(context, plugin_class, plugin_module):
    # Assuming the module is defined in the parent of the tests directory
    sys.path.insert(0, os.path.abspath(os.path.join(context._root['config'].base_dir,'..')))
    module = importlib.import_module(plugin_module)
    context.plugin_class = getattr(module, plugin_class)


@given('we use the HTTP recordings from {filename}')
def step_impl_use_http_recordings(context, filename):
    if 'cassette' in context:
        context.cassette.__exit__()
    file_name = os.path.join(context._root['config'].base_dir,'vcr_cassettes',filename)
    print(f'using cassette at {file_name}')
    my_vcr = vcr.VCR(
        record_mode='none'
    )

    context.cassette = my_vcr.use_cassette(file_name)
    context.cassette.__enter__()

@then('the response will be')
def step_impl_response_will_be(context):
    column_names = []
    row_strings = []
    column_bindings = []
    expected_result = table_to_dataframe(context.table)
    expected_result = expected_result.sort_values(by=['IDENTIFIER']).sort_index(axis=1).reset_index(drop=True)
    context.apply_result = context.apply_result.sort_values(by=['IDENTIFIER']).sort_index(axis=1).reset_index(drop=True)
    # because behave tables work best with a string representation of json, we'll convert the results objects to string
    #expected_result['RESULT'] = expected_result['RESULT'].apply(json.dumps)
    context.apply_result['RESULT'] = context.apply_result['RESULT'].apply(json.dumps)
    assert list(expected_result.columns)==list(context.apply_result.columns),f"Column headings didn't match. Expected: {expected_result.columns}, actual: {context.apply_result.columns}"
    pandas.set_option('display.max_columns', 10)
    pandas.set_option('display.width', 150)
    print(f"expected_result: {expected_result}")
    print(f"expected_result single: {expected_result['RESULT'][0]}")
    print(f"expected_result dtypes: {expected_result.dtypes}")
    print(f"apply_result: {context.apply_result}")
    print(f"apply_result single: {context.apply_result['RESULT'][0]}")
    print(f"apply_result dtypes: {context.apply_result.dtypes}")
    print(f"differences: {expected_result.compare(context.apply_result)}")
    case.assertCountEqual(expected_result.columns.to_list(),context.apply_result.columns.to_list())
    assert_frame_equal(expected_result,context.apply_result)

@then('no error will be raised')
def step_impl_no_error(context):
    assert context.error is None,f"Expected no error from action, instead got {context.error}"