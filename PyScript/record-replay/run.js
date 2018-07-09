const CDP = require('chrome-remote-interface');
const fs = require('fs')

let loaded = 0;

let id_url = {};
let received_time = {};
let load = {};

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
                console.log(`${params.response.url}\t${params.response.timing.receiveHeadersEnd - params.response.timing.sendEnd}`);
            }
        });
    } 
    else {
        Network.responseReceived( (param) => {
            if (param.response.timing != null){
                let url = param.response.url;
                id_url[param.requestId] = url;
                console.log(`Sent\t${param.requestId}\t${url}\t${param.response.timing.requestTime}`);
            }
        });
        Network.dataReceived( (param) => {
            received_time[param.requestId] = param.timestamp;
        });
    }
    /* else {
        Network.requestWillBeSent((params) => {
            //request[params.requestId] = params.request.url;
            console.log(`${params.request.method}\t${params.request.url}`);
        });
    }*/

    Network.loadingFinished( (param) => {
        loaded += 1;
        load[param.requestId] = 1;
    });
    Page.loadEventFired(async () => {
        client.close();
        if (process.argv[3] != "true") {
            let reqId;
            for (reqId in load){
                if (reqId in id_url){
                    console.log(`Received\t${reqId}\t${id_url[reqId]}\t${received_time[reqId]}`);
                }
            }

            console.log(`Loaded: ${loaded}`);
            /*const {data} = await Page.captureScreenshot();
            fs.writeFile(process.argv[3] + '.png', Buffer.from(data, 'base64'), (err) => {
                if (err) throw err;

                //console.log("ScreenShot saved!");
            });*/
        }
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
