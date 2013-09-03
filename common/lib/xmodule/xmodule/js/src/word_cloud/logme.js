define('logme', [], function () {
    var debugMode;

    // debugMode can be one of the following:
    //
    //     true - All messages passed to logme will be written to the internal
    //            browser console.
    //     false - Suppress all output to the internal browser console.
    //
    // Obviously, if anywhere there is a direct console.log() call, we can't do
    // anything about it. That's why use logme() - it will allow to turn off
    // the output of debug information with a single change to a variable.
    debugMode = true;

    return logme;

    /*
     * function: logme
     *
     * A helper function that provides logging facilities. We don't want
     * to call console.log() directly, because sometimes it is not supported
     * by the browser. Also when everything is routed through this function.
     * the logging output can be easily turned off.
     *
     * logme() supports multiple parameters. Each parameter will be passed to
     * console.log() function separately.
     *
     */
    function logme() {
        var i;

        if (
            (typeof debugMode === 'undefined') ||
            (debugMode !== true) ||
            (typeof window.console === 'undefined')
        ) {
            return;
        }

        for (i = 0; i < arguments.length; i++) {
            window.console.log(arguments[i]);
        }
    } // End-of: function logme
});
