import dash_bootstrap_components as dbc


class Accordion(dbc.Accordion):
    """An Accordion component.
A self contained Accordion component. Build up the children using the
AccordionItem component.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- active_item (string; optional):
    The item_id of the currently active item. If item_id has not been
    specified for the active item, this will default to item-i, where
    i is the index (starting from 0) of the item.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  Often used with CSS to
    style elements with common properties.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- flush (boolean; optional):
    Renders accordion edge-to-edge with its parent container.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

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

- persisted_props (list of a value equal to: 'active_item's; default ['active_item']):
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

- start_collapsed (boolean; default False):
    Set to True for all items to be collapsed initially.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    def __init__(self, children=None, **accordion_props):
        accordion_props = accordion_props.copy() if accordion_props else {}
        style = accordion_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        accordion_props['style'] = default_style
        super().__init__(children=children, **accordion_props)

class AccordionItem(dbc.AccordionItem):
    """An AccordionItem component.
A component to build up the children of the accordion.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  Often used with CSS to
    style elements with common properties.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- item_id (string; optional):
    Optional identifier for item used for determining which item is
    visible if not specified, and AccordionItem is being used inside
    Accordion component, the itemId will be set to \"item-i\" where i
    is (zero indexed) position of item in list items pased to
    Accordion component.

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

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- title (string; optional):
    The title on display in the collapsed accordion item."""
    def __init__(self, children=None, **accordionitem_props):
        accordionitem_props = accordionitem_props.copy() if accordionitem_props else {}
        style = accordionitem_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        accordionitem_props['style'] = default_style
        super().__init__(children=children, **accordionitem_props)
