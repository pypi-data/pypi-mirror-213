from dash import dcc

tabs_styles = {
    'height': '52px',
    'width': '2240px'
}

tab_style1 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'padding': '13px',
    'color': '#000000',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_selected_style1 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #003FE2',
    'backgroundColor': '#F2F2F8',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_disabled_style2 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #ebebed',
    'padding': '13px',
    'color': '#858d97',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_style2 = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-family': 'Inter',
    'backgroundColor': '#FFFFFF',
}

tab_selected_style2 = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#0000c9',
    'color': 'white',
    'padding': '6px',
    'font-family': 'Inter'
}

tab_style3 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_selected_style3 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_style4 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_selected_style4 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}


class Tab(dcc.Tab):
    """A Tabs component.
    A Dash component that lets you render pages with tabs - the Tabs component's children
    can be dcc.Tab components, which can hold a label that will be displayed as a tab, and can in turn hold
    children components that will be that tab's content.

    Keyword arguments:

    - children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional):
        Array that holds Tab components.

    - id (string; optional):
        The ID of this component, used to identify dash components in
        callbacks. The ID needs to be unique across all of the components
        in an app.

    - className (string; optional):
        Appends a class to the Tabs container holding the individual Tab
        components.

    - colors (dict; default {    border: '#d6d6d6',    primary: '#1975FA',    background: '#f9f9f9',}):
        Holds the colors used by the Tabs and Tab components. If you set
        these, you should specify colors for all properties, so: colors: {
        border: '#d6d6d6',    primary: '#1975FA',    background: '#f9f9f9'
        }.

        `colors` is a dict with keys:

        - background (string; optional)

        - border (string; optional)

        - primary (string; optional)

    - content_className (string; optional):
        Appends a class to the Tab content container holding the children
        of the Tab that is selected.

    - content_style (dict; optional):
        Appends (inline) styles to the tab content container holding the
        children of the Tab that is selected.

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

    - mobile_breakpoint (number; default 800):
        Breakpoint at which tabs are rendered full width (can be 0 if you
        don't want full width tabs on mobile).

    - parent_className (string; optional):
        Appends a class to the top-level parent container holding both the
        Tabs container and the content container.

    - parent_style (dict; optional):
        Appends (inline) styles to the top-level parent container holding
        both the Tabs container and the content container.

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
        Appends (inline) styles to the Tabs container holding the
        individual Tab components.

    - value (string; optional):
        The value of the currently selected Tab.

    - vertical (boolean; default False):
        Renders the tabs vertically (on the side)."""

    def __init__(self,children=None, **tab_props):
        tab_props = tab_props.copy() if tab_props else {}
        style = tab_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        tab_props['style'] = default_style
        super().__init__(children=children,**tab_props)


class TabStyle1(Tab):
    """
    Class representing the 'tabs_styles1' style.

    Style:
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'padding': '13px',
    'color': '#000000',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
    """

    def __init__(self, children=None, **tab_props):
        tab_props['style'] = tab_style1
        tab_props['selected_style'] = tab_selected_style1
        super().__init__(children=children, **tab_props)


class Disabled_tab(Tab):
    """
    Class representing the 'tabs_styles2' style.

    Style:
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-family': 'Inter',
    'backgroundColor': '#FFFFFF',
    """

    def __init__(self, children=None, **tab_props):
        tab_props['style'] = tab_style2
        tab_props['selected_style'] = tab_selected_style2
        tab_props['tab_disabled_style2'] = tab_disabled_style2
        super().__init__(children=children, **tab_props)


class TabStyle3(Tab):
    """
    Class representing the 'tabs_styles3' style.

    Style:
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
    """

    def __init__(self, children=None, **tab_props):
        tab_props['style'] = tab_style3
        tab_props['selected_style'] = tab_selected_style3
        super().__init__(children=children, **tab_props)


class TabStyle4(Tab):
    """
    Class representing the 'tab_style4' style.

    Style:
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
    """

    def __init__(self, children=None, **tab_props):
        tab_props['style'] = tab_style4
        tab_props['selected_style'] = tab_selected_style4
        super().__init__(children=children, **tab_props)
