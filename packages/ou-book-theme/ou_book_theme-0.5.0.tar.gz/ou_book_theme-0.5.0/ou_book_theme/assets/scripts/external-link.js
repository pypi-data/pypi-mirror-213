/**
 * Ensure all external links open in a new tab.
 */
export function externalLinkSetup() {
    for (const externalLink of document.querySelectorAll('a.reference.external')) {
        externalLink.setAttribute('target', '_blank');
    }
}
