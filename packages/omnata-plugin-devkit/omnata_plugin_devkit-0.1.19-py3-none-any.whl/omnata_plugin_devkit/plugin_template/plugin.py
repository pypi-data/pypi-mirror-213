from omnata_plugin_runtime.forms import InboundSyncConfigurationForm, StreamLister,OutboundSyncConfigurationForm, DynamicFormOptionsDataSource, FormFieldMappingSelector, ConnectionMethod,FormInputField,FormOption,StaticFormOptionsDataSource,FormDropdownField,FormSshKeypair,FormTextAreaField,FormCheckboxField,NewOptionCreator
from omnata_plugin_runtime.omnata_plugin import InboundSyncRequest, OmnataPlugin, PluginManifest, ConnectResponse, OutboundSyncRequest
from omnata_plugin_runtime.configuration import CreateSyncStrategy,UpsertSyncStrategy,UpsertSyncStrategy,DeleteSyncStrategy,OutboundSyncConfigurationParameters,ConnectionConfigurationParameters,InboundSyncConfigurationParameters,OutboundSyncStrategy,OutboundSyncAction
from typing import List
import logging
logger = logging.getLogger('omnata_plugin')

class TemplateApp(OmnataPlugin):
    """
    Omnata Plugin for TemplateApp
    """
    def __init__(self):
        """
        The plugin class for TemplateApp
        """
        OmnataPlugin.__init__(self)
    
    def get_manifest(self) -> PluginManifest:
        return PluginManifest(
            app_id='template_app',
            name='TemplateApp',
            docs_url='',
            supports_inbound=True,
            supported_outbound_strategies=[
                    CreateSyncStrategy(),
                    UpsertSyncStrategy()]
        )

    def connection_form(self) -> List[ConnectionMethod]:
        """
        Returns one or more ConnectionMethod objects, each of which define a form for
        the user to complete during the connection process.
        """
    
    def connect(self, parameters: ConnectionConfigurationParameters) -> ConnectResponse:
        """
        Takes the parameters that the user entered in the connection form and tests the connection.
        Alternatively, the ConnectResponse can contain OAuth parameters which will initiate an OAuth flow.
        """

    def outbound_configuration_form(self,parameters: OutboundSyncConfigurationParameters) -> OutboundSyncConfigurationForm:
        pass

    def sync_outbound(self,parameters: OutboundSyncConfigurationParameters,outbound_sync_request:OutboundSyncRequest):
        """
        Applies a set of changed records to an app. This function is called whenever a run occurs and changed records
        are found.
        To return results, invoke outbound_sync_request.enqueue_results() during the load process.

        :param PluginConfigurationParameters parameters the parameters of the sync, as configured by the user
        :param OutboundSyncRequest outbound_sync_request an object describing what has changed
        :return None
        :raises ValueError: if issues were encountered during connection
        """

    def inbound_configuration_form(self,parameters:InboundSyncConfigurationParameters) -> InboundSyncConfigurationForm:
        pass

    def sync_inbound(self,parameters: InboundSyncConfigurationParameters,inbound_sync_request:InboundSyncRequest):
        """
        Retrieves the next set of records from an application.
        The inbound_sync_request contains the list of streams to be synchronized.
        To return results, invoke inbound_sync_request.enqueue_results() during the load process.

        :param PluginConfigurationParameters parameters the parameters of the sync, as configured by the user
        :param InboundSyncRequest inbound_sync_request an object describing what needs to be sync'd
        :return None
        :raises ValueError: if issues were encountered during connection
        """
