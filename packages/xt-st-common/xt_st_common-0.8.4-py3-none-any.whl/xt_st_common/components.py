import streamlit as st

from xt_st_common.config import StreamlitBaseSettings

settings = StreamlitBaseSettings()


def page_header(
    page_title: str | None = None,
    page_logo: str | None = None,
    page_logo_width: int = 250,
    logout_url: str | None = None,
):
    """
    Display the page header including Title, Logo, and optional Logout button
    """
    base_url = settings.STREAMLIT_SERVER_BASE_URL_PATH
    script_frame = st.empty()
    if logout_url is not None:
        # Load the css/icons for the button
        st.markdown(
            """
            <style scoped type="text/css">
                .btn-logout {
                    box-shadow:inset 0px 1px 0px 0px #ffffff;
                    background:linear-gradient(to bottom, #f9f9f9 5%, #e9e9e9 100%);
                    background-color:#f9f9f9;
                    border-radius:6px;
                    border:1px solid #dcdcdc;
                    display:inline-block;
                    cursor:pointer;
                    color:#666666 !important;
                    font-family:Arial;
                    font-size:15px;
                    padding:4px 20px !important;
                    text-decoration:none;
                    text-shadow:0px 1px 0px #ffffff;
                }
                .btn-logout:hover {
                    background:linear-gradient(to bottom, #e9e9e9 5%, #f9f9f9 100%);
                    background-color:#e9e9e9;
                }
                .btn-logout:active {
                    position:relative;
                    top:1px;
                }
                .main .block-container {
                    padding-top: 3rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Define the button
        logout_link = f'<a id="logout-button" class="btn-logout" href={logout_url} role="button">🔐 Log out</a>'
    else:
        logout_link = "&nbsp;"

    page_title = "" if page_title is None else page_title

    page_logo = "" if page_logo is None else f"<img src='{page_logo}' width='{page_logo_width}px'>"
    # Display the page header including Title, Logo, and optional Logout button
    st.markdown(
        f"""
        <style scoped type="text/css">
            .xt_logo {{
                border-bottom: 1px solid black;
                width: 100%;
                height: 65px;
                margin-bottom: 12px
            }}
            .app_logo{{
                font-family: Consolas, monaco, monospace;
                font-size:200%;
                font-weight:500;
            }}
            .app_logo::after {{
                font-family: sans-serif;
                font-size: small;
                content: '{settings.APP_TAG_TEXT}';
                display: inline-block;
                text-align: center;
                color: white;
                background-color: {settings.APP_TAG_BACKGROUND};
                border-radius: 20px;
                margin-left: -15px;
                padding: 0px 15px;
                font-weight: bold;
                vertical-align: super;
            }}
        </style>
        """
        + f"""
        <div class='xt_logo' >
            <span style='float: right;'>
            {logout_link}
            <img src='{base_url}/app/static/media/XT_words_wrapped.png' width='200px'>
            </span>
            <span class='app_logo'>
        """
        + page_logo
        + page_title
        + """
         </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Attach a function to clear the Cognito cookies when the logout button is clicked
    if settings.USE_COGNITO and len(settings.COGNITO_COOKIE) > 0:
        from streamlit_js_eval import streamlit_js_eval

        # Attach and onClick event handler to the logout button/link
        # When the user logs out the handler will remove cookies which are prefixed with
        # `settings.COGNITO_COOKIE`.
        # Also take the opportunity to have the signout button use the current window rather
        # than opening a new one.
        logout_script = (
            """
                var a = window.parent.document.getElementById("logout-button");
                a.onclick = function() {
                    all_cookies = Object.fromEntries(document.cookie.split('; ').map(c => c.split('=')))
                    cookie_list = Object.keys(all_cookies).filter(key => key.startsWith('"""
            + settings.COGNITO_COOKIE
            + """'))
                    cookie_list.forEach(e => {
                        window.parent.document.cookie = e+'=; expires=Thu, 01 Jan 1970 00:00:01 GMT'
                    })
                    return true;
                }
                // Override the target so that we reload the current page rather than opening a new one
                a.target = ""
            """
        )
        with script_frame:
            streamlit_js_eval(js_expressions=logout_script, key="js-logout-script")
