from dash import html

button_small = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                "flex-direction": "row", "justify-content": "center", "align-item": "center",
                "padding": "7px 16px", "gap": "8px", "position": "relative", "width": "103px",
                "height": "32px", "background": "#003FE2", "border-radius": "1px",
                "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                "color": "#FFFFFF", "border": "none"}

button_medium = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                 "flex-direction": "row", "justify-content": "center", "align-item": "center",
                 "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "119px",
                 "height": "48px", "background": "#003FE2", "border-radius": "1px",
                 "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                 "color": "#FFFFFF", "border": "none"}

button_large = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                "flex-direction": "row", "justify-content": "center", "align-item": "center",
                "padding": "16px 32px", "gap": "12px", "position": "relative", "width": "153px",
                "height": "56px", "background": "#003FE2", "border-radius": "1px",
                "font-weight": "700", "font-size": "17px", "line-height": "24px", "letter-spacing": "-0.5px",
                "color": "#FFFFFF", "border": "none"}

button_xss_icon = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                   "flex-direction": "row", "justify-content": "center", "align-item": "center",
                   "padding": "10px", "position": "relative", "width": "40px",
                   "height": "40px", "background": "#003FE2", "border-radius": "1px",
                   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                   "color": "#FFFFFF", "border": "none"}

button_primary = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                  "flex-direction": "row", "justify-content": "center", "align-item": "center",
                  "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                  "height": "48px", "background": "#003FE2", "border-radius": "1px",
                  "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                  "color": "#FFFFFF", "border": "none"}

button_secondary = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                    "flex-direction": "row", "justify-content": "center", "align-item": "center",
                    "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                    "height": "48px", "background": "#ffffff", "border-radius": "1px",
                    "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                    "color": "#003FE2", "border": "1px solid #003FE2"}

button_tertiary = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                   "flex-direction": "row", "justify-content": "center", "align-item": "center",
                   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                   "height": "48px", "background": "#66BFFF", "border-radius": "1px",
                   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                   "color": "#FFFFFF", "border": "none"}

button_transparent = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                      "flex-direction": "row", "justify-content": "center", "align-item": "center",
                      "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                      "height": "48px", "background": "transparent", "border-radius": "1px",
                      "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                      "color": "#003FE2", "border": "none"}

button_warning = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                  "flex-direction": "row", "justify-content": "center", "align-item": "center",
                  "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                  "height": "48px", "background": "#E84C4E", "border-radius": "1px",
                  "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                  "color": "#FFFFFF", "border": "none"}

button_floating = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                   "flex-direction": "row", "justify-content": "center", "align-item": "center",
                   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                   "height": "48px", "background": "#003FE2", "border-radius": "91px",
                   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                   "color": "#FFFFFF", "border": "none"}


class Button(html.Button):
    """A Button.py component.
    Button.py is a wrapper for the <button> HTML5 element.
    For detailed attribute info see:
    https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button

    Keyword arguments:

    - children (a list of or a singular dash component, string or number; optional):
        The children of this component.

    - id (string; optional):
        The ID of this component, used to identify dash components in
        callbacks. The ID needs to be unique across all of the components
        in an app.

    - accessKey (string; optional):
        Keyboard shortcut to activate or add focus to the element.

    - aria-* (string; optional):
        A wildcard aria attribute.

    - autoFocus (a value equal to: 'autoFocus', 'autofocus', 'AUTOFOCUS' | boolean; optional):
        The element should be automatically focused after the page loaded.

    - className (string; optional):
        Often used with CSS to style elements with common properties.

    - contentEditable (string; optional):
        Indicates whether the element's content is editable.

    - contextMenu (string; optional):
        Defines the ID of a <menu> element which will serve as the
        element's context menu.

    - data-* (string; optional):
        A wildcard data attribute.

    - dir (string; optional):
        Defines the text direction. Allowed values are ltr (Left-To-Right)
        or rtl (Right-To-Left).

    - disable_n_clicks (boolean; optional):
        When True, this will disable the n_clicks prop.  Use this to
        remove event listeners that may interfere with screen readers.

    - disabled (a value equal to: 'disabled', 'DISABLED' | boolean; optional):
        Indicates whether the user can interact with the element.

    - draggable (string; optional):
        Defines whether the element can be dragged.

    - form (string; optional):
        Indicates the form that is the owner of the element.

    - formAction (string; optional):
        Indicates the action of the element, overriding the action defined
        in the <form>.

    - formEncType (string; optional):
        If the button/input is a submit button (e.g. type=\"submit\"),
        this attribute sets the encoding type to use during form
        submission. If this attribute is specified, it overrides the
        enctype attribute of the button's form owner.

    - formMethod (string; optional):
        If the button/input is a submit button (e.g. type=\"submit\"),
        this attribute sets the submission method to use during form
        submission (GET, POST, etc.). If this attribute is specified, it
        overrides the method attribute of the button's form owner.

    - formNoValidate (a value equal to: 'formNoValidate', 'formnovalidate', 'FORMNOVALIDATE' | boolean; optional):
        If the button/input is a submit button (e.g. type=\"submit\"),
        this boolean attribute specifies that the form is not to be
        validated when it is submitted. If this attribute is specified, it
        overrides the novalidate attribute of the button's form owner.

    - formTarget (string; optional):
        If the button/input is a submit button (e.g. type=\"submit\"),
        this attribute specifies the browsing context (for example, tab,
        window, or inline frame) in which to display the response that is
        received after submitting the form. If this attribute is
        specified, it overrides the target attribute of the button's form
        owner.

    - hidden (a value equal to: 'hidden', 'HIDDEN' | boolean; optional):
        Prevents rendering of given element, while keeping child elements,
        e.g. script elements, active.

    - key (string; optional):
        A unique identifier for the component, used to improve performance
        by React.js while rendering components See
        https://reactjs.org/docs/lists-and-keys.html for more info.

    - lang (string; optional):
        Defines the language used in the element.

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

    - name (string; optional):
        Name of the element. For example used by the server to identify
        the fields in form submits.

    - role (string; optional):
        Defines an explicit role for an element for use by assistive
        technologies.

    - spellCheck (string; optional):
        Indicates whether spell checking is allowed for the element.

    - style (dict; optional):
        Defines CSS styles which will override styles previously set.

    - tabIndex (string; optional):
        Overrides the browser's default tab order and follows the one
        specified instead.

    - title (string; optional):
        Text to be displayed in a tooltip when hovering over the element.

    - type (string; optional):
        Defines the type of the element.

    - value (string; optional):
        Defines a default value which will be displayed in the element on
        page load."""

    def __init__(self,children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children,**button_props)


class ButtonSmall(Button):
    """
    Class representing the 'button_small' style.

    Style:
   "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
   "flex-direction": "row", "justify-content": "center", "align-item": "center",
   "padding": "7px 16px", "gap": "8px", "position": "relative", "width": "103px",
   "height": "32px", "background": "#003FE2", "border-radius": "1px",
   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
   "color": "#FFFFFF", "border": "none"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_small
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)


class ButtonMedium(Button):
    """
    Class representing the 'button_medium' style.

    Style:
       "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
       "flex-direction": "row", "justify-content": "center", "align-item": "center",
       "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "119px",
       "height": "48px", "background": "#003FE2", "border-radius": "1px",
       "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
       "color": "#FFFFFF", "border": "none"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_medium
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)


class ButtonLarge(Button):
    """
    Class representing the 'button_large' style.

    Style:
        "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
        "flex-direction": "row", "justify-content": "center", "align-item": "center",
        "padding": "16px 32px", "gap": "12px", "position": "relative", "width": "153px",
        "height": "56px", "background": "#003FE2", "border-radius": "1px",
        "font-weight": "700", "font-size": "17px", "line-height": "24px", "letter-spacing": "-0.5px",
        "color": "#FFFFFF", "border": "none"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_large
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)


class ButtonXssIcon(Button):
    """
    Class representing the 'button_xss_icon' style.

    Style:
   "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
   "flex-direction": "row", "justify-content": "center", "align-item": "center",
   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "119px",
   "height": "48px", "background": "#003FE2", "border-radius": "1px",
   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
   "color": "#FFFFFF", "border": "none"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_xss_icon
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)


class ButtonPrimary(Button):
    """
    Class representing the 'button_primary' style.

    Style:
   "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
   "flex-direction": "row", "justify-content": "center", "align-item": "center",
   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "119px",
   "height": "48px", "background": "#003FE2", "border-radius": "1px",
   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
   "color": "#FFFFFF", "border": "none"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_primary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)


class ButtonSecondary(Button):
    """
    Class representing the 'button_secondary' style.

    Style:
   "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
   "flex-direction": "row", "justify-content": "center", "align-item": "center",
   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
   "height": "48px", "background": "#ffffff", "border-radius": "1px",
   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
   "color": "#003FE2", "border": "1px solid #003FE2"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_secondary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)


class ButtonTertiary(Button):
    """
    Class representing the 'button_tertiary' style.

    Style:
   "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
   "flex-direction": "row", "justify-content": "center", "align-item": "center",
   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
   "height": "48px", "background": "#66BFFF", "border-radius": "1px",
   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
   "color": "#FFFFFF", "border": "none"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_tertiary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)


class ButtonTransparent(Button):
    """
    Class representing the 'button_transparent' style.

    Style:
   "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
   "flex-direction": "row", "justify-content": "center", "align-item": "center",
   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
   "height": "48px", "background": "transparent", "border-radius": "1px",
   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
   "color": "#003FE2", "border": "none"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_transparent
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)


class ButtonWarning(Button):
    """
    Class representing the 'button_warning' style.

    Style:
   "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
   "flex-direction": "row", "justify-content": "center", "align-item": "center",
   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
   "height": "48px", "background": "#E84C4E", "border-radius": "1px",
   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
   "color": "#FFFFFF", "border": "none"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_warning
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)


class ButtonFloating(Button):
    """
    Class representing the 'button_floating' style.

    Style:
   "background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
   "flex-direction": "row", "justify-content": "center", "align-item": "center",
   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
   "height": "48px", "background": "#003FE2", "border-radius": "91px",
   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
   "color": "#FFFFFF", "border": "none"
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_floating
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        super().__init__(children=children, **button_props)
