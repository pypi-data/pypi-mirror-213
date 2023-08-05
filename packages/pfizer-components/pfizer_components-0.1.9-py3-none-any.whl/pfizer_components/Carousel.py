import dash_bootstrap_components as dbc

custom_style = {
    "width": "100%",
    "height": "100%",
    "background-color": "lightgray",
    "border": "1px solid black",
    "padding": "10px",
    "border-radius": "5px"
}


class Carousel(dbc.Carousel):
    """A Carousel component.
Component for creating Bootstrap carousel.  This component is a slideshow
for cycling through a series of content.

Keyword arguments:

- id (string; optional):
    The ID of the component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- active_index (number; default 0):
    The current visible slide number.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  efines the className of
    the carousel container. Often used with CSS to style elements with
    common properties.

- class_name (string; optional):
    Defines the className of the carousel container. Often used with
    CSS to style elements with common properties.

- controls (boolean; default True):
    Show the Carousel previous and next arrows for changing the
    current slide.

- indicators (boolean; default True):
    Show a set of slide position indicators.

- interval (number; optional):
    the interval at which the carousel automatically cycles (default:
    5000) If set to None, carousel will not Autoplay (i.e. will not
    automatically cycle).

- items (list of dicts; required):
    The items to display on the slides in the carousel.

    `items` is a list of dicts with keys:

    - alt (string; optional):
        The alternate text for an image, if the image cannot be
        displayed.

    - caption (string; optional):
        The caption of the item.  The text is displayed in a <p>
        element.

    - captionClassName (string; optional):
        **DEPRECATED** Use `caption_class_name` instead.  The class
        name for the header and caption container.

    - caption_class_name (string; optional):
        The class name for the header and caption container.

    - header (string; optional):
        The header of the text on the slide. It is displayed in a <h5>
        element.

    - imgClassName (string; optional):
        **DEPRECATED** Use `img_class_name` instead.  The className
        for the image.  The default is 'd-block w-100'.

    - img_class_name (string; optional):
        The className for the image.  The default is 'd-block w-100'.

    - img_style (dict; optional):
        The style for the image.

    - key (string; optional):
        A unique identifier for the slide, used to improve performance
        by React.js while rendering components See
        https://reactjs.org/docs/lists-and-keys.html for more info.

    - src (string; optional):
        The URL of the image.

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

- ride (a value equal to: 'carousel'; optional):
    Autoplays the carousel after the user manually cycles the first
    item. If \"carousel\", autoplays the carousel on load.

- slide (boolean; optional):
    controls whether the slide animation on the Carousel works or not.

- style (dict; optional):
    Defines CSS styles of the carousel container. Will override styles
    previously set.

- variant (a value equal to: 'dark'; optional):
    Add `variant=\"dark\"` to the Carousel for darker controls,
    indicators, and captions."""

    def __init__(self, children=None, **carousel_props):
        carousel_props = carousel_props.copy() if carousel_props else {}
        style = carousel_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        carousel_props['style'] = default_style
        super().__init__(children=children, **carousel_props)


class CustomCarousel(Carousel):
    """
    Class representing the 'CustomCarousel' style.

    Style:
    - width: 100%
    - height: 100%
    - background-color: lightgray
    - border: 1px solid black
    - padding: 10px
    - border-radius: 5px
    """

    def __init__(self, children=None, **carousel_props):
        carousel_props = carousel_props.copy() if carousel_props else {}
        style = carousel_props.pop('style', None)
        default_style = custom_style
        if style is not None:
            default_style.update(style)
        carousel_props['style'] = default_style
        super().__init__(children=children, **card_props)
