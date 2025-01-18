import streamlit as st
import streamlit.components.v1 as components

def init_cookie_manager():
    """Initialize the cookie consent manager"""
    
    # Add cookie consent styling
    st.markdown("""
        <style>
        .cookie-banner {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #f8f9fa;
            padding: 1rem;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .cookie-banner button {
            background-color: #1E88E5;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
        }
        
        .analytics-placeholder {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize cookie consent state
    if 'cookie_consent' not in st.session_state:
        st.session_state.cookie_consent = False

def show_cookie_banner():
    """Display the cookie consent banner if consent hasn't been given"""
    if not st.session_state.cookie_consent:
        cookie_banner = """
        <div class="cookie-banner" id="cookieBanner">
            <div>
                This site uses cookies for analytics. By continuing to use this site, you agree to our use of cookies.
                <button onclick="acceptCookies()">Accept</button>
                <button onclick="declineCookies()">Decline</button>
            </div>
        </div>
        <script>
            function acceptCookies() {
                document.getElementById('cookieBanner').style.display = 'none';
                window.parent.postMessage({type: 'cookie_consent', value: true}, '*');
            }
            
            function declineCookies() {
                document.getElementById('cookieBanner').style.display = 'none';
                window.parent.postMessage({type: 'cookie_consent', value: false}, '*');
            }
        </script>
        """
        st.markdown(cookie_banner, unsafe_allow_html=True)

def handle_cookie_consent():
    """Handle cookie consent messages and state"""
    # Handle cookie consent message from JavaScript
    components.html("""
        <script>
            window.addEventListener('message', function(e) {
                if (e.data.type === 'cookie_consent') {
                    const searchParams = new URLSearchParams(window.location.search);
                    searchParams.set('cookie_consent', e.data.value);
                    window.history.replaceState({}, '', '?' + searchParams.toString());
                    window.location.reload();
                }
            });
        </script>
        """, height=0)

    # Update session state based on URL parameter
    try:
        params = st.experimental_get_query_params()
        if 'cookie_consent' in params:
            st.session_state.cookie_consent = params['cookie_consent'][0] == 'true'
    except:
        pass

def load_analytics():
    """Load analytics scripts if consent is given"""
    if st.session_state.cookie_consent:
        components.html("""
            <!-- Google Analytics -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=UA-122023594-8"></script>
            <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', 'UA-122023594-8');
            </script>
            
            <!-- HubSpot Analytics -->
            <script type="text/javascript" id="hs-script-loader" async defer src="//js.hs-scripts.com/6571207.js"></script>
        """, height=0)