const CDP = require('chrome-remote-interface');
const fs = require('fs')
const url = require('url')
const path = require('path')

let loaded = 0;
let onload = null;

// Used for first time difference
let firstWillBeSent = false;
let firstSent = false;
let reqWillBeSent = null;
let reqSent = null;

let id_url = {};
let load = {};

let end = null;
let begin = null;

let url_NWT = {}; // { url: [reqWillBeSent, loadingFinish]
let first_received = {};

let logs = [];

function compare(a, b){
    if (a[0] == b[0]){
        return a[1] - b[1];
    }
    return a[0] - b[0];
}


function list_stringify(li){
    str = "";
    for (let i in li){
        str += `[${li[i].join(", ")}]\n`;
    }
    return str;
}

function union(li) {
    let length = li.length;
    let final = [li[0]];
    //console.log(list_stringify(li));
    let NWT = 0;
    for (let i = 1; i < length; i++){
        let interval = li[i];
        if (interval[0] <= final.slice(-1)[0][1]){
            final[final.length-1][1] = Math.max(interval[1], final[final.length-1][1]);
        } else {
            final.push(interval);
        }
    }
    // console.log("After union: ");
    //console.log(list_stringify(final));
    for (let i = 0; i < final.length; i++){
        NWT += final[i][1] - final[i][0];
    }
    return NWT;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

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
        /*Network.emulateNetworkConditions({
            offline: false,
            latency: 0,
            downloadThroughput: 1024/8,
            uploadThroughput: 1024*1024*9/8,
            connectionType: 'cellular4g'
        });*/
        Network.responseReceived( (param) => {
            param['eventType'] = 'responseReceived';
            // if (param.response.timing != null){
            //     console.log(`Response Received: ${id_url[param.requestId]}\t${param.response.timing.requestTime}`);
            // }
            if (!firstSent){
                reqSent = param.response.timing.requestTime;
                firstSent = true;
            }
            //console.log(`responseReceived\t${param.requestId}\t${id_url[param.requestId]}\t${param.timestamp}`);
            logs.push(param);
            if (param.response.timing != null){
                url_NWT[param.requestId] = [param.response.timing.sendStart/1000 + param.response.timing.requestTime];
            }
            // first_received[param.requestId] = [param.timestamp, timing1, timing2];
        });

        Network.requestWillBeSent( (param) => {
            param['eventType'] = 'requestWillBeSent';
            if (!firstWillBeSent) {
                reqWillBeSent = param.timestamp;
                firstWillBeSent = true;
            }
            id_url[param.requestId] = param.request.url;
            // url_NWT[param.requestId] = [param.timestamp];
            //console.log(`requestWillBeSent\t${param.requestId}\t${id_url[param.requestId]}\t${param.timestamp}`);
            logs.push(param);
        });

        // Network.dataReceived( (param)=> {
        //     last_received[param.requestId] = param.timestamp;
        //     console.log(`Data received: ${id_url[param.requestId]}\t${param.timestamp}`);
        // });

        Network.loadingFinished( (param) => {
            param['eventType'] = 'loadingFinished';
            if (onload != null){
                return;
            }
            loaded += 1;
            load[param.requestId] = 1;
            //console.log(`Loading Finished: ${param.requestId}\t${id_url[param.requestId]}\t${param.timestamp}\t${ param.requestId in url_NWT}`);
            if (param.requestId in url_NWT){
                url_NWT[param.requestId].push(param.timestamp);
                logs.push(param);
                //url_NWT[param.requestId].push(url.parse(id_url[param.requestId]).hostname);
                //url_NWT[param.requestId].push(param.timestamp);
                // url_NWT[param.requestId].push(first_received[param.requestId][2]);
            }
            // if (param.requestId in id_url){
            //     console.log(`loadingFinished\t${param.requestId}\t${id_url[param.requestId]}\t${param.timestamp}`);
            // }
        });
    }


    Page.loadEventFired( (param) => {
        client.close();
        if (process.argv[3] != "true") {
            onload = param.timestamp;
            end = Date.now();

            console.log(`Loaded: ${loaded}`);

            for (let id in url_NWT){
                if (url_NWT[id].length < 2){
                    delete url_NWT[id];
                } else if (url_NWT[id][1] > onload) {
                    url_NWT[id][1] = onload;
                }
            }

            let NWT = Object.values(url_NWT);
            NWT = NWT.sort(compare);
            /*const {data} = await Page.captureScreenshot();
            fs.writeFile(process.argv[3] + '.png', Buffer.from(data, 'base64'), (err) => {
                if (err) throw err;

                //console.log("ScreenShot saved!");
            });*/

            fs.appendFile(path.join('plTime', process.argv[3]), `PLT\t${ (end-begin)/1000 }\nNWT\t${ union(NWT) }\n`, (err) => {
                if (err) throw err;
            });
            fs.writeFile(path.join('network_log', process.argv[3] + '-' + process.argv[4] + '.json'), JSON.stringify(logs), 'utf-8', err=>{
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

