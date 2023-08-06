# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class GooglePicker(Component):
    """A GooglePicker component.
GooglePicker Component.

This component provides a Google file picker for the application.
The picker provides access to files stored in Google Drive.

Props:
@prop {string} id - A unique identifier for the component.
@prop {function} setProps - Function to update component's props.
@prop {bool} open - Determines if the picker is opened or not.
@prop {(string|array)} view_ids - Google View IDs to be displayed in the picker.
@prop {string} client_id - The client_id of the Google Cloud application.
@prop {string} scope - The scopes for the Google Cloud application.
@prop {string} developer_key - The developer key of the Google Cloud application.
@prop {(string|array)} enabled_features - Features to enable in the picker.
@prop {(string|array)} disabled_features - Features to disable in the picker.
@prop {string} locale - The locale to be used in the picker.
@prop {string} action - The current action performed in the picker.
@prop {array} documents - The documents selected from the picker.

State:
@state {bool} pickerInited - Indicates if the Google Picker API has been loaded.
@state {bool} gisInited - Indicates if the Google Sign-in API has been loaded.
@state {string} accessToken - The access token received from Google Sign-in.
@state {bool} open - Determines if the picker is opened or not.
@state {bool} pendingPicker - Indicates if there is a pending picker creation.

Default Props:
@default {bool} open - false
@default {array} view_ids - ['all']
@default {string} scope - 'https://www.googleapis.com/auth/drive.readonly'
@default {array} enabled_features - []
@default {array} disabled_features - []
@default {string} locale - null
@default {string} action - ''
@default {null} documents - null

Methods:
@method loadGoogleApi - Loads Google API script.
@method loadGoogleGsiClient - Loads Google Sign-in script.
@method onApiLoad - Callback for Google API load.
@method gisLoaded - Callback for Google Sign-in load.
@method createPicker - Creates the Google Picker.
@method pickerCallback - Callback for Google Picker actions.

Keyword arguments:

- id (string; required):
    A unique identifier for the component.

- action (string; default ''):
    The current action performed in the picker.

- client_id (string; required):
    The client_id of the Google Cloud application.

- developer_key (string; required):
    The developer key of the Google Cloud application.

- disabled_features (string | list of strings; optional):
    Features to disable in the picker.

- documents (list of dicts; optional):
    The documents selected from the picker.

- enabled_features (string | list of strings; optional):
    Features to enable in the picker.

- locale (string; optional):
    The locale to be used in the picker.

- open (boolean; default False):
    Determines if the picker is opened or not.

- scope (string; default 'https://www.googleapis.com/auth/drive.readonly'):
    The scopes for the Google Cloud application.

- view_ids (string | list of strings; default ['all']):
    Google View IDs to be displayed in the picker."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_google_picker'
    _type = 'GooglePicker'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, open=Component.UNDEFINED, view_ids=Component.UNDEFINED, client_id=Component.REQUIRED, scope=Component.UNDEFINED, developer_key=Component.REQUIRED, enabled_features=Component.UNDEFINED, disabled_features=Component.UNDEFINED, locale=Component.UNDEFINED, action=Component.UNDEFINED, documents=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'action', 'client_id', 'developer_key', 'disabled_features', 'documents', 'enabled_features', 'locale', 'open', 'scope', 'view_ids']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'action', 'client_id', 'developer_key', 'disabled_features', 'documents', 'enabled_features', 'locale', 'open', 'scope', 'view_ids']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'client_id', 'developer_key']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(GooglePicker, self).__init__(**args)
