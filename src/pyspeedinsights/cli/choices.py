
# Limit cmd line arg choices based on API query param options.
COMMAND_CHOICES = {
    'category': [
        'accessibility', 'best-practices', 
        'performance', 'pwa', 'seo'
    ],
    'strategy': [
        'desktop', 'mobile'
    ],
    'locale': [
        'ar', 'bg', 'ca', 'zh-TW', 'zh-CN', 'hr', 'cs', 'da', 'nl',
        'en', 'en-GB', 'fil', 'fi', 'fr', 'de', 'el', 'iw', 'hi', 'hu',
        'id', 'it', 'ja', 'ko', 'lv', 'lt', 'no', 'pl', 'pt-BR', 'pt-PT',
        'ro', 'ru', 'sr', 'sk', 'sl', 'es', 'sv', 'th', 'tr', 'uk', 'vi',
    ],
    'format': [
        'json', 'excel', 'sitemap'
    ],
    # `all` is used as an arg to include all metrics in the Excel output
    'metrics': [
        "all",
        "observedTotalCumulativeLayoutShift",
        "observedCumulativeLayoutShift",
        "observedLargestContentfulPaintAllFrames",
        "maxPotentialFID",
        "observedSpeedIndexTs",
        "observedFirstContentfulPaintTs",
        "observedTimeOrigin",
        "observedFirstPaint",
        "observedNavigationStartTs",
        "observedLargestContentfulPaintAllFramesTs",
        "speedIndex",
        "observedFirstContentfulPaint",
        "observedLastVisualChangeTs",
        "cumulativeLayoutShiftMainFrame",
        "observedLastVisualChange",
        "cumulativeLayoutShift",
        "largestContentfulPaint",
        "observedDomContentLoaded",
        "firstContentfulPaint",
        "observedCumulativeLayoutShiftMainFrame",
        "observedFirstVisualChange",
        "observedFirstPaintTs",
        "totalCumulativeLayoutShift",
        "observedFirstMeaningfulPaint",
        "interactive",
        "observedTraceEnd",
        "observedFirstMeaningfulPaintTs",
        "totalBlockingTime",
        "observedFirstContentfulPaintAllFramesTs",
        "observedLargestContentfulPaint",
        "observedNavigationStart",
        "observedLoad",
        "observedFirstVisualChangeTs",
        "observedFirstContentfulPaintAllFrames",
        "observedTimeOriginTs",
        "observedTraceEndTs",
        "observedLoadTs",
        "observedDomContentLoadedTs",
        "observedSpeedIndex",
        "firstMeaningfulPaint",
        "observedLargestContentfulPaintTs"
    ]
}
