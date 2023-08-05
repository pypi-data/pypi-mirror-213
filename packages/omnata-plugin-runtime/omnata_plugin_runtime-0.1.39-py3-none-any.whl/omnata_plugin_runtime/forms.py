# it's not the 1980s anymore
# pylint: disable=line-too-long,multiple-imports,logging-fstring-interpolation,too-many-arguments,no-self-argument
"""
Contains form elements for Omnata plugin configuration
"""
from __future__ import annotations
import sys
from typing import List,Callable, Literal, Union, ForwardRef, Optional
if tuple(sys.version_info[:2]) >= (3, 9):
    # Python 3.9 and above
    from typing import Annotated
else:
    # Python 3.8 and below
    from typing_extensions import Annotated
from abc import ABC
from types import MethodType
from pydantic import BaseModel,Field,validator # pylint: disable=no-name-in-module
from .configuration import SubscriptableBaseModel, StreamConfiguration, SyncConfigurationParameters, InboundSyncConfigurationParameters

class FormOption(SubscriptableBaseModel):
    """
    An option used by certain form forms (like Dropdowns).

    :param str value: The value to set in the field if this option is selected
    :param str label: The label to show in the list. This value is not stored.
    :param dict metadata: An arbitrary dictionary to store with the value, which can be retrieved by the plugin
    :param bool required: When populating field mapping options, this flag indicates that this field is mandatory
    :param bool unique: When populating field mapping options, this flag indicates that this field requires a unique value (i.e. be mapped from a unique column)
    :param bool default: Indicates that this option should be the default selected
    :param bool disabled: Indicates that the option should appear in the list, but be unselectable
    :param str data_type_icon: The data type icon to show next to the option (where applicable)
    :return: nothing
    """
    value:str
    label:str
    metadata:dict = Field(default_factory=dict)
    required:bool=False
    unique:bool=False
    default:bool=False
    disabled:bool=False
    data_type_icon:str='unknown'

class FormInputField(SubscriptableBaseModel):
    """
    An input field, which collects a single line of free-form text from the user and no metadata.
    """
    name:str
    label:str
    default_value:Union[str,bool]=''
    required:bool=False
    depends_on:str=None
    help_text:str=""
    reload_on_change:bool=False
    secret:bool=False
    type:Literal['input'] = 'input'

class FormTextAreaField(SubscriptableBaseModel):
    """
    A text area field, which collects multi-line free-form text from the user and no metadata.

    :param str name: The name of the form field. This value must be unique, and is used to retrieve the value from within the plugin code.
    :param str label: The label for the form field
    :param str default_value: The default value presented initially in the field
    :param bool required: If True, means that the form cannot be submitted without a value present
    :param str depends_on: The name of another form field. If provided, this form field will not be rendered until there is a value in the field it depends on.
    :param str help_text: A longer description of what the field is used for. If provided, a help icon is shown and must be hovered over to display this text.
    :param bool secret: Indicates that the text entered must be masked in the browser, and stored/access securely
    :param bool reload_on_change: If True, the entire form is reloaded after the value is changed. This is used to conditionally render fields based on values provided in others, but should be used only when strictly necessary.
    :return: nothing
    """
    name:str
    label:str
    default_value:str=''
    secret:bool=False
    required:bool=False
    depends_on:str=None
    help_text:str=""
    reload_on_change:bool=False
    type:Literal['textarea'] = 'textarea'

    variables:bool=False

class FormSshKeypair(SubscriptableBaseModel):
    """
    An SSH Keypair field, which generates public and private keys for asymmetric cryptography.
    """
    name:str
    label:str
    default_value:str=None
    required:bool=False
    depends_on:str=None
    help_text:str=""
    
    type:Literal['ssh_keypair'] = 'ssh_keypair'
    secret:bool=True

class FormCheckboxField(SubscriptableBaseModel):
    """
    A field which presents a checkbox
    """
    name:str
    label:str
    default_value:bool=False
    required:bool=False
    secret:bool=False
    depends_on:str=None
    help_text:str=""
    reload_on_change:bool=False
    type:Literal['checkbox'] = 'checkbox'

class FormSliderField(SubscriptableBaseModel):
    """
    A field which presents a slider
    """
    name:str
    label:str
    default_value:str=None
    secret:bool=False
    required:bool=False
    depends_on:str=None
    help_text:str=""
    reload_on_change:bool=False
    type:Literal['slider'] = 'slider'

    min_value:int=0
    max_value:int=100
    step_size:int=1

class StreamLister(SubscriptableBaseModel):
    """
    A class for managing the listing of Streams. Can depend on other form fields to delay rendering
    """
    source_function:Union[Callable[[InboundSyncConfigurationParameters], List[StreamConfiguration]],str]
    label:str="Select Objects"
    depends_on:str=None

    @validator('source_function', always=True)
    def function_name_convertor(cls, v, values) -> str:
        return v.__name__ if isinstance(v,MethodType) else v

class FormJinjaTemplate(SubscriptableBaseModel):
    """
    Uses text area to allow the user to create a template, which can include column values from the source
    """
    mapper_type:Literal["jinja_template"] = 'jinja_template'
    label:str="Jinja Template"
    label:str=None
    depends_on:str=None

# ----------------------------------------------------------------------------
# Everything above here has no dependencies on other BaseModels in this module
# ----------------------------------------------------------------------------

NewOptionCreator = ForwardRef('NewOptionCreator')

class StaticFormOptionsDataSource(SubscriptableBaseModel):
    """
    A Data Source for providing a static set of form options

    :param List[FormOption] values: The list of values to return
    :param NewOptionCreator new_option_creator: If provided, it means that values can be added to the datasource via the provided mechanism
    :return: nothing
    """
    values:List[FormOption] = Field(default_factory=list)
    new_option_creator:NewOptionCreator = None
    type:Literal["static"] = 'static'

class DynamicFormOptionsDataSource(SubscriptableBaseModel):
    """
    A Data Source for providing a set of form options that load dynamically from the server
    """
    source_function:Union[Callable[[SyncConfigurationParameters], List[FormOption]],str]
    new_option_creator:NewOptionCreator = None
    type:Literal["dynamic"] = 'dynamic'

    @validator('source_function', always=True)
    def function_name_convertor(cls, v, values) -> str:
        return v.__name__ if isinstance(v,MethodType) else v

FormOptionsDataSourceBase = Annotated[Union[StaticFormOptionsDataSource,DynamicFormOptionsDataSource], Field(discriminator='type')]

class FormFieldWithDataSource(SubscriptableBaseModel):
    """
    Denotes that the field uses a data source
    """
    data_source:FormOptionsDataSourceBase

class FormRadioField(FormFieldWithDataSource,BaseModel):
    """
    A field which presents a set of radio options
    :param str name: The name of the form field. This value must be unique, and is used to retrieve the value from within the plugin code.
    :param str label: The label for the form field
    :param FormOptionsDataSourceBase data_source provides the values for the radio group
    :param str default_value: The default value presented initially in the field
    :param bool required: If True, means that the form cannot be submitted without a value present
    :param str depends_on: The name of another form field. If provided, this form field will not be rendered until there is a value in the field it depends on.
    :param str help_text: A longer description of what the field is used for. If provided, a help icon is shown and must be hovered over to display this text.
    :param bool reload_on_change: If True, the entire form is reloaded after the value is changed. This is used to conditionally render fields based on values provided in others, but should be used only when strictly necessary.
    :return: nothing
    """
    name:str
    label:str
    default_value:str=None
    required:bool=False
    secret:bool=False
    depends_on:str=None
    help_text:str=""
    reload_on_change:bool=False
    type:Literal['radio'] = 'radio'

class FormDropdownField(FormFieldWithDataSource,BaseModel):
    """
    A field which presents a dropdown list of options

    """
    name:str
    label:str
    default_value:str=None
    required:bool=False
    secret:bool=False
    depends_on:str=None
    help_text:str=""
    reload_on_change:bool=False
    type:Literal['dropdown'] = 'dropdown'

    multi_select:bool=False

FormFieldBase = Annotated[Union[FormInputField,FormTextAreaField,FormSshKeypair,FormRadioField,FormCheckboxField,FormSliderField,FormDropdownField], Field(discriminator='type')]

class ConfigurationFormBase(BaseModel,ABC):
    """
    Defines a form for configuring a sync. Includes zero or more form fields.

    :param List[FormFieldBase] fields: A list of fields to display to the user
        :return: nothing
    """
    fields:List[FormFieldBase]

class NewOptionCreator(SubscriptableBaseModel):
    """
    Allows for options to be added to a datasource by the user.
    It does this by presenting the user with a form, then building a FormOption from the provided values.
    """
    creation_form_function:Union[Callable[[SyncConfigurationParameters], ConfigurationFormBase],str]
    creation_complete_function:Union[Callable[[SyncConfigurationParameters], FormOption],str]
    allow_create:bool = True

    @validator('creation_form_function', always=True)
    def function_name_convertor(cls, v, values) -> str:
        return v.__name__ if isinstance(v,MethodType) else v

    @validator('creation_complete_function', always=True)
    def function_name_convertor_2(cls, v, values) -> str:
        return v.__name__ if isinstance(v,MethodType) else v

StaticFormOptionsDataSource.update_forward_refs()
DynamicFormOptionsDataSource.update_forward_refs()

class FormFieldMappingSelector(FormFieldWithDataSource,BaseModel):
    """
    Uses a visual column->field mapper, to allow the user to define how source columns map to app fields

    :param FormOptionsDataSourceBase data_source: A data source which provides the app field options
    :param str depends_on: Provide the name of another field to make it dependant, so that the mapper won't display until a value has been provided
    :return: nothing
        """
    mapper_type:Literal["field_mapping_selector"] = 'field_mapping_selector'
    label:str="Field Mappings"
    depends_on:str=None


Mapper = Annotated[Union[FormFieldMappingSelector,FormJinjaTemplate], Field(discriminator='mapper_type')]

class OutboundSyncConfigurationForm(ConfigurationFormBase):
    """
    Defines a form for configuring an outbound sync.
    Includes the zero or more form fields from the base class, and optionally a column->field mapper
    to map Snowflake columns to app fields/payloads.
    """
    mapper:Optional[Mapper] = None

class InboundSyncConfigurationForm(ConfigurationFormBase):
    """
    Defines a form for configuring an inbound sync.
    Includes the zero or more form fields from the base class, and then a means of displaying stream information.
    """
    fields:List[FormFieldBase] = Field(default_factory=list)
    stream_lister:StreamLister
    
class ConnectionMethod(SubscriptableBaseModel):
    """
    Defines a method of connecting to an application.
    :param str data_source: The name of the connection method, e.g. "OAuth", "API Key", "Credentials"
    :param List[FormFieldBase] fields: A list of fields that are used to collect the connection information from the user.
    :param List[str] network_addresses: A list of URLs that will be added to a network rule to permit outbound access from Snowflake
        for the authentication step. Note that for OAuth Authorization flows, it is not necessary to provide the
        initial URL that the user agent is directed to.
    :param bool oauth: If True, the resulting form will indicate to the user that OAuth will be used. 
        In this scenario, the oauth_parameters function will be called before the connect function.
    """
    name:str
    fields:List[FormFieldBase]
    network_addresses:List[str]
    oauth:bool=False


