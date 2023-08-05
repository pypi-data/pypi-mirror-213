
import dash_bootstrap_components as dbc


modal_style = {
    "box-shadow": "0px 20px 25px -5px rgba(0, 0, 0, 0.1), 0px 8px 10px -6px rgba(0, 0, 0, 0.1)",
    "border-radius": "1px",
}

modal_header_style = {"background-color": "#003FE2", "color": "white"}


class Modal(dbc.Modal):
    """A Modal component.
Create a toggleable dialog using the Modal component. Toggle the visibility
with the `is_open` prop.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- autoFocus (boolean; optional):
    **DEPRECATED** Use `autofocus` instead          Puts the focus on
    the modal when initialized.

- autofocus (boolean; optional):
    Puts the focus on the modal when initialized.

- backdrop (boolean | a value equal to: 'static'; optional):
    Includes a modal-backdrop element. Alternatively, specify 'static'
    for a backdrop which doesn't close the modal on click.

- backdropClassName (string; optional):
    **DEPRECATED** Use `backdrop_class_name` instead  CSS class to
    apply to the backdrop.

- backdrop_class_name (string; optional):
    CSS class to apply to the backdrop.

- centered (boolean; optional):
    If True, vertically center modal on page.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  Often used with CSS to
    style elements with common properties.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- contentClassName (string; optional):
    **DEPRECATED** Use `content_class_name` instead  CSS class to
    apply to the modal content.

- content_class_name (string; optional):
    CSS class to apply to the modal content.

- fade (boolean; optional):
    Set to False for a modal that simply appears rather than fades
    into view.

- fullscreen (a value equal to: PropTypes.bool, PropTypes.oneOf(['sm-down', 'md-down', 'lg-down', 'xl-down', 'xxl-down']); optional):
    Renders a fullscreen modal. Specifying a breakpoint will render
    the modal as fullscreen below the breakpoint size.

- is_open (boolean; optional):
    Whether modal is currently open.

- keyboard (boolean; optional):
    Close the modal when escape key is pressed.

- labelledBy (string; optional):
    **DEPRECATED** Use `labelledby` instead  The ARIA labelledby
    attribute.

- labelledby (string; optional):
    The ARIA labelledby attribute.

- modalClassName (string; optional):
    **DEPRECATED** Use `modal_class_name` instead  CSS class to apply
    to the modal.

- modal_class_name (string; optional):
    CSS class to apply to the modal.

- role (string; optional):
    The ARIA role attribute.

- scrollable (boolean; optional):
    It True, scroll the modal body rather than the entire modal when
    it is too long to all fit on the screen.

- size (string; optional):
    Set the size of the modal. Options sm, lg, xl for small, large or
    extra large sized modals, or leave undefined for default size.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- tag (string; optional):
    HTML tag to use for the Modal, default: div.

- zIndex (number | string; optional):
    **DEPRECATED** Use `zindex` instead  Set the z-index of the modal.
    Default 1050.

- zindex (number | string; optional):
    Set the z-index of the modal. Default 1050.

- Defualt styles used for this are :
    box-shadow: 0px 20px 25px -5px rgba(0, 0, 0, 0.1), 0px 8px 10px -6px rgba(0, 0, 0, 0.1)
    border-radius: 1px,
    """
    def __init__(self, children=None, **modal_props):
        style = modal_props.pop('style', None)
        default_style = modal_style
        if style is not None:
            default_style.update(style)
        modal_props['style'] = default_style
        super().__init__(children=children, **modal_props)


class ModalHeader(dbc.ModalHeader):
    """A ModalHeader component.
Add a header to any modal.

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

- close_button (boolean; default True):
    Add a close button to the header that can be used to close the
    modal.

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

- tag (string; optional):
    HTML tag to use for the ModalHeader, default: div.

- Defualt styles used for this are :
    background-color: #003FE2
     color: white
    """
    def __init__(self, children=None, **modalheader_props):
        style = modalheader_props.pop('style', None)
        default_style = modal_header_style
        if style is not None:
            default_style.update(style)
        modalheader_props['style'] = default_style
        super().__init__(children=children, **modalheader_props)


class ModalBody(dbc.ModalBody):
    """A ModalBody component.
Use this component to add consistent padding to the body (main content) of
your Modals.

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

- tag (string; optional):
    HTML tag to use for the ModalBody, default: div."""
    def __init__(self, children=None, **modalbody_props):
        style = modalbody_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        modalbody_props['style'] = default_style
        super().__init__(children=children, **modalbody_props)


class ModalFooter(dbc.ModalFooter):
    """A ModalFooter component.
Add a footer to any modal.

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

- tag (string; optional):
    HTML tag to use for the ModalFooter, default: div."""
    def __init__(self, children=None, **modalfooter_props):
        style = modalfooter_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        modalfooter_props['style'] = default_style
        super().__init__(children=children, **modalfooter_props)

