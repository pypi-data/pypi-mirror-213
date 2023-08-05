import dash_bootstrap_components as dbc

information_toast_style = {"background": "#4C5459", "color": "white"}
success_toast_style = {"background": "#8DC248", "color": "black"}
warning_toast_style = {"background": "##FFCF00", "color": "black"}
error_toast_style = {"background": "#E84C4E", "color": "black"}


class Toast(dbc.Toast):
    """A Toast component.
Toasts can be used to push messages and notifactions to users. Control
visibility of the toast with the `is_open` prop, or use `duration` to set a
timer for auto-dismissal.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- bodyClassName (string; optional):
    **DEPRECATED** - use `body_class_name` instead.  Often used with
    CSS to style elements with common properties. The classes
    specified with this prop will be applied to the body of the toast.

- body_class_name (string; optional):
    Often used with CSS to style elements with common properties. The
    classes specified with this prop will be applied to the body of
    the toast.

- body_style (dict; optional):
    Defines CSS styles which will override styles previously set. The
    styles set here apply to the body of the toast.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  Often used with CSS to
    style elements with common properties.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- color (string; optional):
    Toast color, options: primary, secondary, success, info, warning,
    danger, light, dark. Default: secondary.

- dismissable (boolean; default False):
    Set to True to add a dismiss button to the header which will close
    the toast on click.

- duration (number; optional):
    Duration in milliseconds after which the Alert dismisses itself.

- header (string; optional):
    Text to populate the header with.

- headerClassName (string; optional):
    **DEPRECATED** - use `header_class_name` instead  Often used with
    CSS to style elements with common properties. The classes
    specified with this prop will be applied to the header of the
    toast.

- header_class_name (string; optional):
    Often used with CSS to style elements with common properties. The
    classes specified with this prop will be applied to the header of
    the toast.

- header_style (dict; optional):
    Defines CSS styles which will override styles previously set. The
    styles set here apply to the header of the toast.

- icon (string; optional):
    Add a contextually coloured icon to the header of the toast.
    Options are: \"primary\", \"secondary\", \"success\", \"warning\",
    \"danger\", \"info\", \"light\" or \"dark\".

- is_open (boolean; default True):
    Whether Toast is currently open.

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

- n_dismiss (number; default 0):
    An integer that represents the number of times that the dismiss
    button has been clicked on.

- n_dismiss_timestamp (number; default -1):
    Use of *_timestamp props has been deprecated in Dash in favour of
    dash.callback_context. See \"How do I determine which Input has
    changed?\" in the Dash FAQs https://dash.plot.ly/faqs.  An integer
    that represents the time (in ms since 1970) at which n_dismiss
    changed. This can be used to tell which button was changed most
    recently.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- tag (string; optional):
    HTML tag to use for the Toast, default: div."""

    def __init__(self, children=None, **toast_props):
        toast_props = toast_props.copy() if toast_props else {}
        style = toast_props.pop('style', None)
        default_style = {
            "width": "320px",
            "color": "white",
            "background": "#4C5459",
            "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.25)",
            "border-radius": "1px"
        }
        if style is not None:
            default_style.update(style)
        toast_props['style'] = default_style

        header_style = toast_props.pop('header_style', None)
        default_header_style = {"background": "#4C5459"}
        if header_style is not None:
            default_header_style.update(header_style)
        toast_props['header_style'] = default_header_style
        super().__init__(children=children, **toast_props)


class InformationalToast(Toast):
    """
    Class representing the 'InformationalToast' style.

    Style/Header Style:

    background: #4C5459
    color: white
    """

    def __init__(self, children=None, **toast_props):
        toast_props['style'] = information_toast_style
        toast_props['header_style'] = information_toast_style
        super().__init__(children=children, **toast_props)


class SuccessToast(Toast):
    """
    Class representing the 'SuccessToast' style.

    Style/Header Style:

    background: #8DC248
    color: black
    """

    def __init__(self, children=None, **toast_props):
        toast_props['style'] = success_toast_style
        toast_props['header_style'] = success_toast_style
        super().__init__(children=children, **toast_props)


class WarningToast(Toast):
    """
    Class representing the 'WarningToast' style.

    Style/Header Style:

    background: #FFCF00
    color: black
    """

    def __init__(self, children=None, **toast_props):
        toast_props['style'] = warning_toast_style
        toast_props['header_style'] = warning_toast_style
        super().__init__(children=children, **toast_props)


class ErrorToast(Toast):
    """
    Class representing the 'ErrorToast' style.

    Style/Header Style:

    background: #E84C4E
    color: black
    """

    def __init__(self, children=None, **toast_props):
        toast_props['style'] = error_toast_style
        toast_props['header_style'] = warning_toast_style
        super().__init__(children=children, **toast_props)
