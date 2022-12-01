import os
import random
import zipfile
import random
import pytz

from selenium import webdriver
from time import sleep

class MyChrome:
    def __init__(self):
        self.driver = None

    def getTimeZone(self):
        return random.choice(pytz.all_timezones)

    def antiDetectJS(self):
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                        Object.defineProperty(window, 'deviceMemory', {
                                    get: () => Math.floor(Math.random() * 10),
                        });

                        """
            },
        )

    def getPlugin(self, proxy_host, proxy_port, proxy_user, proxy_pass, sl):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy_host, proxy_port, proxy_user, proxy_pass)
        try:
            os.remove(f'.\\extension\\proxy{sl}.zip')
        except: pass
        pluginfile = f'.\\extension\\proxy{sl}.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        
        return pluginfile
    
    def randomCardName(self):
        listCard = ['Nvidia RTX 3090 Ti', 'Nvidia RTX 3090', 'Nvidia RTX 3080 Ti', 'Nvidia RTX 3080', 'Nvidia Quadro RTX A6000', 'Nvidia Quadro RTX A5000', 'Nvidia RTX 3070 Ti', 'Nvidia Titan V', 'Nvidia RTX 3070', 'Nvidia RTX 3080 [Laptop]', 'Nvidia RTX 2080 Ti', 'Nvidia RTX Titan', 'Nvidia RTX 3060 Ti', 'Nvidia RTX 3070 [Laptop]', 'Nvidia RTX 3060', 'Nvidia Titan Pascal', 'Nvidia RTX 2080 SUPER', 'Nvidia RTX 3060 [Laptop]', 'Nvidia GTX 1080 Ti', 'Nvidia RTX 2080',
                    'Nvidia Quadro RTX A4000', 'Nvidia RTX 2070 SUPER', 'Nvidia RTX 2070', 'Nvidia RTX 2060 SUPER', 'Nvidia RTX 2060', 'Nvidia GTX 1080', 'Nvidia RTX 3050', 'Nvidia GTX 1070 Ti', 'Nvidia RTX 3050 Ti [Laptop]', 'Nvidia GTX 980 Ti', 'Nvidia GTX 1070', 'Nvidia GTX 1660 Ti', 'Nvidia GTX 1660 SUPER', 'Nvidia RTX 3050 [Laptop]', 'Nvidia GTX 1660', 'Nvidia GTX 1060', 'Nvidia GTX 980', 'Nvidia GTX 1650 SUPER', 'Nvidia GTX 1650', 'Nvidia GTX 1050 Ti', 'Nvidia GTX 960', 'Nvidia GTX 1050']
        return random.choice(listCard)

    def getUserAgent(self):
        try:
            user = [us.strip("\n") for us in open(".\\UserAgent\\ua.txt","r",encoding="UTF-8").readlines()]
            return random.choice(user)
        except:
            return 'Mozilla/5.0 (Linux; Android 8.1.0; 16th Plus Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.145 Mobile Safari/537.36'
    def OpenChrome(self, proxy, sl, type_prx):
        options = webdriver.ChromeOptions()
        # brave_path = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
        # options.binary_location = brave_path
        if type_prx == 'socks5':
            options.add_argument('--proxy-server=socks5://%s' % proxy)
        elif type_prx == 'https':
            options.add_argument('--proxy-server=%s' % proxy)
        elif type_prx == 'user_pass':
            ipProxy = proxy.split(':')
            proxy_host = ipProxy[0]
            proxy_port = ipProxy[1]
            proxy_user = ipProxy[2]
            proxy_pass = ipProxy[3]
            proxyArgsList = [
                {
                    'proxy_host': proxy_host,
                    'proxy_port': proxy_port,
                    'proxy_user': proxy_user,
                    'proxy_pass': proxy_pass,
                    'sl':sl
                }
            ]
            options.add_extension(self.getPlugin(**random.choice(proxyArgsList))) # fake proxy
        # options.add_extension('.\\ext\\0.1.3_0.crx')
        # options.add_extension('.\\ext\\0.1.5_0.crx')
        # options.add_extension('.\\ext\\0.1.5.crx')
        # options.add_extension('.\\ext\\0.1.6_0.crx')
        # options.add_extension('.\\ext\\0.1.9_0.crx')
        # options.add_extension('.\\ext\\10.1.1.crx')
        preferences = {
        "webrtc.ip_handling_policy" : "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled" : False
            }
        options.add_experimental_option("prefs", preferences)
        options.add_argument('--disable-webrtc-hw-encoding')
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "exit_type": "none",
            "exited_cleanly": True,
            'profile.default_content_setting_values': {'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                       'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                                       'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                       'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                                       'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                       'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                                                       'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                                                       'durable_storage': 2}
        }
        options.add_experimental_option('prefs', prefs)
        # if vpn == 2:
            # options.add_extension('.\\extension\\vpn.zip')
        options.add_argument("--test-type")
        self.ua = self.getUserAgent()
        # options.add_extension('.\\extension\\WebRTC.zip')
        #
        options.add_argument('--allow-file-access-from-files')
        options.add_argument('--use-file-for-fake-video-capture=video.y4m')
        options.add_argument('--use-file-for-fake-audio-capture=audio.wav')
        options.add_argument('--disable-gpu')
        options.add_argument('--use-fake-ui-for-media-stream')
        #
        options.add_argument('--user-agent={}'.format(self.ua))
        options.add_argument('--disable-blink-features')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-checking-optimization-guide-user-permissions")
        options.add_argument("--disable-shader-name-hashing")
        options.add_argument("--disable-shared-workers")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-logging")
        options.add_argument('--disable-application-cache')
        options.add_argument("--disable-bundled-ppapi-flash")
        options.add_argument("--disable-gaia-services")
        options.add_argument("--disable-gpu-compositing")
        options.add_argument('--disable-signin-scoped-device-id')
        options.add_argument("--disable-gpu-shader-disk-cache")
        options.add_argument('--disable-notifications')
        options.add_argument("--disable-checker-imaging")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-fine-grained-time-zone-detection")
        options.add_argument("--disable-hid-detection-on-oobe")
        options.add_argument("--force-dev-mode-highlighting")
        options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging","disable-popup-blocking"])
        options.add_argument(f"--webgl-rerender=ANGLE ({self.randomCardName()} Direct3D11 vs_5_0 ps_5_0, D3D11)")
        options.add_argument(f"--window-size=220,300")
        options.add_argument("--app=https://dogiloveyou.com/15-fluffy-kittens-who-grew-up-to-become-majestic-floofs/")
        a = ["--disable-background-networking", "--disable-bundled-ppapi-flash", "--disable-client-side-phishing-detection",  "--disable-webgl", "--disable-notifications", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--disable-web-security",
             "--disable-rtc-smoothness-algorithm", "--disable-webrtc-hw-decoding", "--disable-webrtc-hw-encoding", "--disable-webrtc-multiple-routes", "--disable-webrtc-hw-vp8-encoding", "--enforce-webrtc-ip-permission-check", "--force-webrtc-ip-handling-policy", "--ignore-certificate-errors"]
        for i in a:
            options.add_argument(i)
        self.driver = webdriver.Chrome(
            options=options)
        # self.driver.set_page_load_timeout(10)
        # self.driver.implicitly_wait(10)
        # tz_params = {'timezoneId': self.getTimeZone()}
        # self.driver.get("https://iphey.com/")
        # stealth(self.driver,
        #         languages=["en-US", "en"],
        #         vendor="Google Inc. (Intel)",
        #         platform="Win32",
        #         webgl_vendor="Google Inc. (Intel)",
        #         renderer=f"ANGLE ({self.randomCardName()} Direct3D11 vs_5_0 ps_5_0, D3D11)",
        #         fix_hairline=True,
        #         )
        # self.antiDetectJS()
       
        return self.driver, self.ua

    
