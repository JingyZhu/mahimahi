const CDP = require('chrome-remote-interface');
const fs = require('fs')

let loaded = 0;

CDP((client) => {
    // extract domains
    const { Network, Page, Security } = client;
    // console.log(Security);

    Security.setIgnoreCertificateErrors({ ignore: true });
    //Security.disable();

    // setup handlers
    if (process.argv[3] == "true") {
        Network.responseReceived((params) => {
            if (params.response.timing != null) {
                console.log(`${params.response.url}\t${params.response.timing.dnsEnd - params.response.timing.dnsStart + params.response.timing.receiveHeadersEnd - params.response.timing.sendEnd}`);
            }
        });
    } /* else {
        Network.requestWillBeSent((params) => {
            //request[params.requestId] = params.request.url;
            console.log(`${params.request.method}\t${params.request.url}`);
        });
    }*/

    Network.loadingFinished((params) => {
        loaded += 1;
    });
    Page.loadEventFired(async () => {
        if (process.argv[3] != "true") {
            console.log(`Loaded: ${loaded}`);
            const {data} = await Page.captureScreenshot();
            fs.writeFile(process.argv[3] + '.png', Buffer.from(data, 'base64'), (err) => {
                if (err) throw err;

                //console.log("ScreenShot saved!");
            });
        }
        client.close();
    });

    // enable events then start!
    Promise.all([
        Network.enable(),
        Page.enable()
    ]).then(() => {
        return Page.navigate({ url: process.argv[2] });
    }).catch((err) => {
        console.error(err);
        client.close();
    });

}).on('error', (err) => {
    // cannot connect to the remote endpoint
    console.error(err);
});
