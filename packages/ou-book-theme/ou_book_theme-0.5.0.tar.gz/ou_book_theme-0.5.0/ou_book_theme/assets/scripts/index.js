import '../styles/index.scss';
import { activitySetup } from './activity';
import { externalLinkSetup } from './external-link';

function DOMContentLoaded() {
    activitySetup();
    externalLinkSetup();
}

document.addEventListener('DOMContentLoaded', DOMContentLoaded, false);
