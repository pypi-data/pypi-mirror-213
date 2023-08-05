import dash_bootstrap_components as dbc

class Nav(dbc.Nav):
    """A Nav component.
Nav can be used to group together a collection of navigation links.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- card (boolean; optional):
    Set to True when using Nav with pills styling inside a CardHeader.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  Often used with CSS to
    style elements with common properties.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- fill (boolean; optional):
    Expand the nav items to fill available horizontal space.

- horizontal (a value equal to: 'start', 'center', 'end', 'between', 'around'; optional):
    Specify the horizontal alignment of the NavItems. Options are
    'start', 'center', or 'end'.

- justified (boolean; optional):
    Expand the nav items to fill available horizontal space, making
    sure every nav item has the same width.

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

- navbar (boolean; optional):
    Set to True if using Nav in Navbar component. This applies the
    `navbar-nav` class to the Nav which uses more lightweight styles
    to match the parent Navbar better.

- navbar_scroll (boolean; optional):
    Enable vertical scrolling within the toggleable contents of a
    collapsed Navbar.

- pills (boolean; optional):
    Apply pill styling to nav items. Active items will be indicated by
    a pill.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- vertical (boolean | string; optional):
    Stack NavItems vertically. Set to True for a vertical Nav on all
    screen sizes, or pass one of the Bootstrap breakpoints ('xs',
    'sm', 'md', 'lg', 'xl') for a Nav which is vertical at that
    breakpoint and above, and horizontal on smaller screens."""
    def __init__(self, children=None, **nav_props):
        nav_props = nav_props.copy() if nav_props else {}
        style = nav_props.pop('style', None)
        default_style = {
            "width": "1440px",
            "height": "64px",
            "background": "#FFFFFF",
            "border-bottom": "#F2F2F8",
        }
        if style is not None:
            default_style.update(style)
        nav_props['style'] = default_style
        super().__init__(children=children, **nav_props)


class NavItem(dbc.NavItem):
    """A NavItem component.
Create a single item in a `Nav`.

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
    Defines CSS styles which will override styles previously set."""
    def __init__(self, children=None, **navitem_props):
        navitem_props = navitem_props.copy() if navitem_props else {}
        style = navitem_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        navitem_props['style'] = default_style
        super().__init__(children=children, **navitem_props)


class NavLink(dbc.NavLink):
    """A NavLink component.
Add a link to a `Nav`. Can be used as a child of `NavItem` or of `Nav`
directly.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- active (boolean | a value equal to: 'partial', 'exact'; default False):
    Apply 'active' style to this component. Set to \"exact\" to
    automatically toggle active status when the current pathname
    matches href, or to \"partial\" to automatically toggle on a
    partial match. Assumes that href is a relative url such as /link
    rather than an absolute such as https://example.com/link  For
    example - dbc.NavLink(..., href=\"/my-page\", active=\"exact\")
    will be active on   \"/my-page\" but not \"/my-page/other\" or
    \"/random\" - dbc.NavLink(..., href=\"/my-page\",
    active=\"partial\") will be active on   \"/my-page\" and
    \"/my-page/other\" but not \"/random\".

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  Often used with CSS to
    style elements with common properties.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- disabled (boolean; default False):
    Disable the link.

- external_link (boolean; optional):
    If True, the browser will treat this as an external link, forcing
    a page refresh at the new location. If False, this just changes
    the location without triggering a page refresh. Use this if you
    are observing dcc.Location, for instance. Defaults to True for
    absolute URLs and False otherwise.

- href (string; optional):
    The URL of the linked resource.

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

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- n_clicks_timestamp (number; default -1):
    An integer that represents the time (in ms since 1970) at which
    n_clicks changed. This can be used to tell which button was
    changed most recently.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- target (string; optional):
    Target attribute to pass on to the link. Only applies to external
    links."""
    def __init__(self, children=None, **navlink_props):
        navlink_props = navlink_props.copy() if navlink_props else {}
        style = navlink_props.pop('style', None)
        default_style = {'color': 'black'}
        if style is not None:
            default_style.update(style)
        navlink_props['style'] = default_style
        super().__init__(children=children, **navlink_props)
