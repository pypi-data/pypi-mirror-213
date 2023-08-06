/**
 * Enable the toggle button on OU activities.
 */
export function activitySetup() {
    for(const toggle of document.querySelectorAll('.ou-toggle')) {
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('ou-toggle-hidden');
        });
    }
}
