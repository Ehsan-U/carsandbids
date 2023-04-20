# utilities for the spider

def request_should_abort(request):
    return (
        request.resource_type == "image" or ".jpg" in request.url
    )


settings = dict(
    DOWNLOAD_DELAY = 1,
    REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7',
    DOWNLOAD_HANDLERS = {
        "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    },
    TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    PLAYWRIGHT_MAX_CONTEXTS = 8,
    PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 4,
    PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000,
    PLAYWRIGHT_ABORT_REQUEST = request_should_abort,
    PLAYWRIGHT_BROWSER_TYPE = 'firefox',
    FEEDS = {"data/carsandbids.csv": {"format": "csv"}},
    USER_AGENT = None,
    LOG_LEVEL='DEBUG',
)


playwright_args = {
    "playwright": True,
    "playwright_include_page": True,
    "playwright_context_kwargs": {
        "ignore_https_errors": True,
    },
}
