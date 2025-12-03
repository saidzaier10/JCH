export const analytics = {
    trackEvent: (category, action, label = null, value = null) => {
        console.log(`[Analytics] Event: ${category} - ${action}`, { label, value })
        // Integration with Google Analytics or Plausible would go here
        // if (window.gtag) { window.gtag('event', action, { event_category: category, event_label: label, value: value }) }
    },
    trackPageView: (path) => {
        console.log(`[Analytics] Page View: ${path}`)
        // if (window.gtag) { window.gtag('config', 'GA_MEASUREMENT_ID', { page_path: path }) }
    }
}
