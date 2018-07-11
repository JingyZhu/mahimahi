const CDP = require('chrome-remote-interface');
const fs = require('fs')

let loaded = 0;

let firstWillBeSent = false;
let firstSent = false;

let reqWillBeSent = null;
let reqSent = null;

let id_url = {};
let received_time = {};
let load = {};

let end = null;
let begin = null;

CDP((client) => {
    // extract domains
    const { Network, Page, Security } = client;
    // console.log(Security);

    Security.setIgnoreCertificateErrors({ ignore: true });
    //Security.disable()

    // setup handlers
    if (process.argv[3] == "true") {
        Network.responseReceived((params) => {
            if (params.response.timing != null) {
                console.log(`${params.response.url}\t${params.response.timing.receiveHeadersEnd - params.response.timing.sendEnd}`);
            }
        });
    } 
    else {
        Network.emulateNetworkConditions({
            offline: false,
            latency: 0,
            downloadThroughput: 1024*1024*9/8,
            uploadThroughput: 1024*1024*9/8,
            connectionType: 'cellular4g'
        });
        Network.responseReceived( (param) => {
            // if (param.response.timing != null){
            //     let url = param.response.url;
            //     id_url[param.requestId] = url;
            //     console.log(`Sent\t${param.requestId}\t${url}\t${param.response.timing.requestTime}`);
            // }
            if (!firstSent){
                reqSent = param.response.timing.requestTime;
                firstSent = true;
            }
        });

        Network.requestWillBeSent( (param) => {
            if (!firstWillBeSent) {
                reqWillBeSent = param.timestamp;
                firstWillBeSent = true;
            }
        });
        // Network.dataReceived( (param) => {
        //     received_time[param.requestId] = param.timestamp;
        // });
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
        received_time[param.requestId] = param.timestamp;
    });
    Page.loadEventFired( (param) => {
        client.close();
        if (process.argv[3] != "true") {
            let reqId;
            end = Date.now();
            // for (reqId in load){
            //     if (reqId in id_url && reqId in  received_time){
            //         console.log(`Received\t${reqId}\t${id_url[reqId]}\t${received_time[reqId]}`);
            //     }
            // }

            console.log(`Loaded: ${loaded}`);
            console.log(`Difference: ${reqSent-reqWillBeSent}`);
            /*const {data} = await Page.captureScreenshot();
            fs.writeFile(process.argv[3] + '.png', Buffer.from(data, 'base64'), (err) => {
                if (err) throw err;

                //console.log("ScreenShot saved!");
            });*/

            fs.appendFile(process.argv[3], `replay\t${ (end-begin)/1000 }\n`, (err) => {
                if (err) throw err;
            });
        }
    });

    // enable events then start!
    Promise.all([
        Network.enable(),
        Page.enable()
    ]).then(() => {
        begin = Date.now();
        return Page.navigate({ url: process.argv[2] });
    }).catch((err) => {
        console.error(err);
        client.close();
    });

}).on('error', (err) => {
    // cannot connect to the remote endpoint
    console.error(err);
});
