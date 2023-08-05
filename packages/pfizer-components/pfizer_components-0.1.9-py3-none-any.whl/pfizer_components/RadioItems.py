import dash_bootstrap_components as dbc

radio_items_style = {'font-family': 'Noto Sans'}


class RadioItems(dbc.RadioItems):
    """A RadioItems component.
RadioItems is a component that encapsulates several radio item inputs.
The values and labels of the RadioItems is specified in the `options`
property and the seleced item is specified with the `value` property.
Each radio item is rendered as an input and associated label which are
siblings of each other.

Keyword arguments:

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  The class of the
    container (div).

- class_name (string; optional):
    The class of the container (div).

- inline (boolean; optional):
    Arrange RadioItems inline.

- inputCheckedClassName (string; optional):
    **DEPRECATED** Use `input_checked_class_name` instead.  Additional
    CSS classes to apply to the <input> element when the corresponding
    radio is checked.

- inputCheckedStyle (dict; optional):
    **DEPRECATED** Use `input_checked_style` instead.  Additional
    inline style arguments to apply to <input> elements on checked
    items.

- inputClassName (string; default ''):
    **DEPRECATED** Use `input_class_name` instead.  The class of the
    <input> radio element.

- inputStyle (dict; optional):
    **DEPRECATED** Use `input_style` instead.  The style of the
    <input> radio element.

- input_checked_class_name (string; optional):
    Additional CSS classes to apply to the <input> element when the
    corresponding radio is checked.

- input_checked_style (dict; optional):
    Additional inline style arguments to apply to <input> elements on
    checked items.

- input_class_name (string; default ''):
    The class of the <input> radio element.

- input_style (dict; optional):
    The style of the <input> radio element.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- labelCheckedClassName (string; optional):
    **DEPRECATED** Use `label_checked_class_name` instead.  Additional
    CSS classes to apply to the <label> element when the corresponding
    radio is checked.

- labelCheckedStyle (dict; optional):
    **DEPRECATED** Use `label_checked_style` instead.  Additional
    inline style arguments to apply to <label> elements on checked
    items.

- labelClassName (string; default ''):
    **DEPRECATED** Use `label_class_name` instead.  CSS classes to
    apply to the <label> element for each item.

- labelStyle (dict; optional):
    **DEPRECATED** Use `label_style` instead.  Inline style arguments
    to apply to the <label> element for each item.

- label_checked_class_name (string; optional):
    Additional CSS classes to apply to the <label> element when the
    corresponding radio is checked.

- label_checked_style (dict; optional):
    Additional inline style arguments to apply to <label> elements on
    checked items.

- label_class_name (string; default ''):
    CSS classes to apply to the <label> element for each item.

- label_style (dict; optional):
    Inline style arguments to apply to the <label> element for each
    item.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- name (string; optional):
    The name of the control, which is submitted with the form data.

- options (list of dicts; optional):
    The options to display as items in the component. This can be an
    array or a dictionary as follows:  \n1. Array of options where the
    label and the value are the same thing - [string|number]  \n2. An
    array of options ``` {   \"label\": [string|number],   \"value\":
    [string|number],   \"disabled\": [bool] (Optional),
    \"input_id\": [string] (Optional),   \"label_id\": [string]
    (Optional) } ```  \n3. Simpler `options` representation in
    dictionary format. The order is not guaranteed. All values and
    labels will be treated as strings. ``` {\"value1\": \"label1\",
    \"value2\": \"label2\", ... } ``` which is equal to ``` [
    {\"label\": \"label1\", \"value\": \"value1\"},   {\"label\":
    \"label2\", \"value\": \"value2\"}, ... ] ```.

    `options` is a list of string | numbers | dict | list of dicts
    with keys:

    - disabled (boolean; optional):
        If True, this radio item is disabled and can't be clicked on.

    - input_id (string; optional):
        id for this option's input, can be used to attach tooltips or
        apply CSS styles.

    - label (a list of or a singular dash component, string or number; required):
        The radio item's label.

    - label_id (string; optional):
        id for this option's label, can be used to attach tooltips or
        apply CSS styles.

    - value (string | number; required):
        The value of the radio item. This value corresponds to the
        items specified in the `value` property.

- persisted_props (list of a value equal to: 'value's; default ['value']):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (boolean | string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- style (dict; optional):
    The style of the container (div).

- switch (boolean; optional):
    Set to True to render toggle-like switches instead of radios.

- value (string | number; optional):
    The currently selected value."""

    def __init__(self,children=None, **radio_items_props):
        radio_items_props = radio_items_props.copy() if radio_items_props else {}
        style = radio_items_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        radio_items_props['style'] = default_style
        super().__init__(children=children,**radio_items_props)


class RadioItemsStyle(RadioItems):
    """
    Class representing the 'radio_items_style' style.

    Style:
    'font-family': 'Noto Sans'
    """

    def __init__(self, children=None, **radio_items_props):
        radio_items_props = radio_items_props.copy() if radio_items_props else {}
        style = radio_items_props.pop('style', None)
        default_style = radio_items_style
        if style is not None:
            default_style.update(style)
        radio_items_props['style'] = default_style
        super().__init__(children=children, **radio_items_props)
