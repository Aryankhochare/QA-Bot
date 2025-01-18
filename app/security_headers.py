from typing import Dict

def get_security_headers() -> Dict[str, str]:
    """Return security headers for the Streamlit app"""
    return {
        'Content-Security-Policy': """
            default-src 'self';
            script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://js.hs-scripts.com;
            style-src 'self' 'unsafe-inline';
            img-src 'self' data: https:;
            connect-src 'self' https://www.google-analytics.com https://js.hs-scripts.com;
            frame-src 'self';
            frame-ancestors 'self';
            form-action 'self';
            base-uri 'self';
            object-src 'none';
        """.replace('\n', ' ').strip(),
        'X-Frame-Options': 'SAMEORIGIN',
        'X-Content-Type-Options': 'nosniff',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': """
            accelerometer=(), ambient-light-sensor=(), autoplay=(), 
            battery=(), camera=(), cross-origin-isolated=(), 
            display-capture=(), document-domain=(), encrypted-media=(),
            execution-while-not-rendered=(), execution-while-out-of-viewport=(),
            fullscreen=(), geolocation=(), gyroscope=(), magnetometer=(), 
            microphone=(), midi=(), navigation-override=(), payment=(), 
            picture-in-picture=(), publickey-credentials-get=(), 
            screen-wake-lock=(), sync-xhr=(), usb=(), web-share=(), 
            xr-spatial-tracking=()
        """.replace('\n', ' ').strip()
    }