import { watchEffect } from 'vue'

export function useSeo(title, description) {
    watchEffect(() => {
        document.title = `${title} | Judo Club Hem`

        let metaDescription = document.querySelector('meta[name="description"]')
        if (!metaDescription) {
            metaDescription = document.createElement('meta')
            metaDescription.setAttribute('name', 'description')
            document.head.appendChild(metaDescription)
        }
        metaDescription.setAttribute('content', description)
    })
}
