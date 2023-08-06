# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashGridmap(Component):
    """A DashGridmap component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    Classname .

- data (list of dicts; required):
    Dataset.

- height (number; optional):
    The value displayed in the input.

- show_axes (boolean; optional):
    Dash-assigned callback that should be called to report property
    changes to Dash, to make them available for callbacks.

- style (dict; optional):
    The value displayed in the input.

- width (number; optional):
    The value displayed in the input."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_gridmap'
    _type = 'DashGridmap'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.REQUIRED, className=Component.UNDEFINED, height=Component.UNDEFINED, style=Component.UNDEFINED, width=Component.UNDEFINED, show_axes=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'data', 'height', 'show_axes', 'style', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'data', 'height', 'show_axes', 'style', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DashGridmap, self).__init__(**args)
