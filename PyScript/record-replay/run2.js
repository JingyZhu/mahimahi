const  CDP = require('chrome-remote-interface');
const fs = require('fs');

CDP(async (client) => {
    try {
        const {Page, Tracing, Security} = client;

        Security.setIgnoreCertificateErrors({ ignore: true });

        // enable Page domain events
        await Page.enable();
        // trace a page load
        const events = [];
        Tracing.dataCollected(({value}) => {
            events.push(...value);
        });
        await Tracing.start();
        await Page.navigate({url: process.argv[2]});
        await Page.loadEventFired();
        await Tracing.end();
        await Tracing.tracingComplete();
        // save the tracing data
        fs.writeFileSync(process.argv[3], JSON.stringify(events));
    } catch (err) {
        console.error(err);
    } finally {
        await client.close();
    }
}).on('error', (err) => {
    console.error(err);
});
