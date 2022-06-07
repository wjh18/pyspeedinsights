"""
Define argpase command line argument choices.

'category', 'strategy' and 'locale' are all based on available PSI API query params.

'format' is specific to pyspeedinsights and dictates the output format of the results.

'metrics' defines available performance metrics to include, with 'all' denoting all metrics.
"""

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
