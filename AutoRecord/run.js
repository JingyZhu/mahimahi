const CDP = require('chrome-remote-interface');


CDP((client) => {
    // extract domains
    const {Network, Page, Security} = client;
    // console.log(Security);

    Security.setIgnoreCertificateErrors({ignore: true});
    //Security.disable();

    // setup handlers
    if (process.argv[3] == "true"){
        Network.responseReceived ((params) => {
            if (params.response.timing != null){
                console.log(`${params.response.url}\t${params.response.timing.receiveHeadersEnd - params.response.timing.sendEnd}`);
            }
        });
    } else {
        Network.requestWillBeSent((params) => {
            console.log(params.request.url);
        });
    }
    Page.loadEventFired(() => {
        client.close();
    });

    // enable events then start!
    Promise.all([
        Network.enable(),
        Page.enable()
    ]).then(() => {
        return Page.navigate({url: process.argv[2]});
    }).catch((err) => {
        console.error(err);
        client.close();
    });

}).on('error', (err) => {
    // cannot connect to the remote endpoint
    console.error(err);
});