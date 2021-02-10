import os


class Chrome_Args:
    def __init__(self):
        self._chrome_args: list = self.get_default_chrome_args()

    def args(self):
        return self._chrome_args

    def args_remove(self, item):
        if item in self._chrome_args:
            self._chrome_args.remove(item)
        return self

    def args_append(self,item):
        if item not in self._chrome_args:
            self._chrome_args.append(item)
        return self

    def args_remove_single_process(self      ): return self.args_remove('--single-process')
    def args_set_user_data_dir    (self, path): return self.args_append('--user-data-dir='+path)

    def get_default_chrome_args(self):
        return [                                # list from https://github.com/alixaxel/chrome-aws-lambda/blob/master/source/index.js#L72
                  '--no-sandbox'            ,   # most important ones
                  #'--disable-dev-shm-usage' ,   # most important ones
                  '--single-process'        ,   # most important ones (this has a nasty side effect when opening up Jira, the redirect crashes chrome)
                  #'--disable-background-timer-throttling',     # already added by puppeteer
                  #'--disable-breakpad',                        # already added by puppeteer
                  #'--disable-client-side-phishing-detection',  # already added by puppeteer
                  '--disable-cloud-import',
                  #'--disable-default-apps',                    # already added by puppeteer
                  #'--disable-extensions',                      # already added by puppeteer
                  '--disable-gesture-typing',
                  #'--disable-hang-monitor',                    # already added by puppeteer
                  '--disable-infobars',
                  '--disable-notifications',
                  '--disable-offer-store-unmasked-wallet-cards',
                  '--disable-offer-upload-credit-cards',
                  #'--disable-popup-blocking',                  # already added by puppeteer
                  '--disable-print-preview',
                  #'--disable-prompt-on-repost',                # already added by puppeteer
                  '--disable-setuid-sandbox',
                  '--disable-speech-api',
                  #'--disable-sync',                            # already added by puppeteer
                  '--disable-tab-for-desktop-share',
                  #'--disable-translate',                       # already added by puppeteer
                  '--disable-voice-input',
                  '--disable-wake-on-wifi',
                  '--disk-cache-size=33554432',
                  '--enable-async-dns',
                  '--enable-simple-cache-backend',
                  '--enable-tcp-fast-open',
                  '--enable-webgl',
                  '--hide-scrollbars',
                  '--ignore-gpu-blacklist',
                  '--media-cache-size=33554432',
                  #'--metrics-recording-only',                  # already added by puppeteer
                  '--mute-audio',
                  '--no-default-browser-check',
                  #'--no-first-run',                            # already added by puppeteer
                  '--no-pings',
                  '--no-zygote',
                  #'--password-store=basic',                    # already added by puppeteer
                  '--prerender-from-omnibox=disabled',
                  '--use-gl=swiftshader',
                  #'--use-mock-keychain',                       # already added by puppeteer
                ]

    def enable_logging(self, log_file=None):
        self.args_append('--enable-logging')
        self.args_append('--v=1')
        if log_file:
            self.set_chrome_log_file(log_file)
        return self

    def set_chrome_log_file(self, path):
        os.putenv('CHROME_LOG_FILE', path)
        return self