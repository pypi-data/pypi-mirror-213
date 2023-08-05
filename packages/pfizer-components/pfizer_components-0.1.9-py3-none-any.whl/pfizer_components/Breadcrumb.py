import dash_bootstrap_components as dbc


class Breadcrumb(dbc.Breadcrumb):
    """A Breadcrumb component.
Use breadcrumbs to create a navigation breadcrumb in your app.

Keyword arguments:

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional):
    **DEPRECATED** - Use class_name instead.  Often used with CSS to
    style elements with common properties.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- itemClassName (string; optional):
    **DEPRECATED** - use item_class_name instead.  Class name ot apply
    to each item.

- item_class_name (string; optional):
    Class name to apply to each item.

- item_style (dict; optional):
    Defines inline CSS styles that will be added to each item in the
    breadcrumbs.

- items (list of dicts; optional):
    The details of the items to render inside of this component.

    `items` is a list of dicts with keys:

    - active (boolean; optional):
        Apply 'active' style to this component.

    - external_link (boolean; optional):
        If True, the browser will treat this as an external link,
        forcing a page refresh at the new location. If False, this
        just changes the location without triggering a page refresh.
        Use this if you are observing dcc.Location, for instance.
        Defaults to True for absolute URLs and False otherwise.

    - href (string; optional):
        URL of the resource to link to.

    - label (string; optional):
        Label to display inside the breadcrumbs.

    - target (string; optional):
        Target attribute to pass on to the link. Only applies to
        external links.

    - title (string; optional):
        title attribute for the inner a element.

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

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- tag (dict; optional):
    HTML tag to use for the outer breadcrumb component. Default:
    \"nav\"."""
    def __init__(self, children=None, **breadcrumb_props):
        breadcrumb_props = breadcrumb_props.copy() if breadcrumb_props else {}
        style = breadcrumb_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        breadcrumb_props['style'] = default_style
        super().__init__(children=children, **breadcrumb_props)
