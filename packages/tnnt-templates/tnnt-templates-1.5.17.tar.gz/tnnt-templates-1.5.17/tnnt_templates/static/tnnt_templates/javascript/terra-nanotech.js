$(document).ready(function () {
    'use strict';

    /**
     * extend links to external website
     * » add target="_blank"
     * » add rel="noopener noreferer"
     */
    let externalLinks = function () {
        // let internalHost = location.hostname.replace(/ /g, '').split(',');
        let internalHost = [location.hostname];
        let protocolPattern = /^https?:\/\//i;

        /**
         * walk through all links on the current page
         */
        $('a').each(function () {
            let href = $(this).attr('href');

            /**
             * check if its a http link
             */
            if (protocolPattern.test(href)) {
                let hrefHostname = $(new URL(href)).attr('hostname');

                if ($.inArray(hrefHostname, internalHost) === -1) {
                    $(this).attr('target', '_blank');
                    $(this).attr('rel', 'noopener noreferer');
                }
            }
        });
    };

    /**
     * check time
     * @param i
     * @returns {string}
     */
    let checkTime = function (i) {
        if (i < 10) {
            i = '0' + i;
        }

        return i;
    };

    /**
     * render a JS clock for Eve Time
     * @param element
     * @param utcOffset
     */
    let renderClock = function (element, utcOffset) {
        let today = new Date();
        let h = today.getUTCHours();
        let m = today.getUTCMinutes();
        let s = today.getUTCSeconds();

        h = h + utcOffset;

        if (h > 24) {
            h = h - 24;
        }

        if (h < 0) {
            h = h + 24;
        }

        h = checkTime(h);
        m = checkTime(m);
        s = checkTime(s);

        // document.getElementById('clock').innerHTML = h + ":" + m + ":" + s;
        element.html(h + ':' + m + ':' + s);

        setTimeout(function () {
            renderClock(element, 0);
        }, 500);
    };

    /**
     * functions that need to be executed on load
     */
    let init = function () {
        externalLinks();
        renderClock($('.eve-time-wrapper .eve-time-clock'), 0);
    };

    /**
     * start the show
     */
    init();

    /**
     * functions that need to be executed on successful ajax events
     */
    $(document).ajaxSuccess(function () {
        externalLinks();
    });
});
