#!/usr/bin/env node
/**
 * Created by wormgear on 2020/07/11.
 */
// import modules
var http = require('http');
var https = require('https');
var url = require('url');
var events = require('events');
//var JSON = require('JSON');
var stats = undefined;
url_today = 'https://covid19-japan-web-api.now.sh/api/v1/total';
url_yesterday = url_today + '?history=true';

http.createServer(function (req, res) {
    function getCoronaVirusStatus(callback) {
        https.get(url_today, function (res) {
            res.on('data', function (d) {
                //process.stdout.write(d);
                callback(JSON.parse(d));
            });
            res.on('error', function (e) {
                console.error(e);
            });
        });
    }

    function coronaVirusStats(results) {
        var newDate = results.date;
        var newPositive = results.positive;
        var newDeath = results.death;
        var newMonth = newDate.toString().split('')[4] + newDate.toString().split('')[5];
        var newDay = newDate.toString().split('')[6] + newDate.toString().split('')[7];
        var objDate = new Date(newMonth).toLocaleString("en-us", { month: "long" });
        var newMonthDay = objDate + ' ' + newDay;
        var coronavirus_stats = "As of " + newMonthDay + " there have been " + String(newPositive) + " confirmed cases, and " + String(newDeath) + " deaths.";
        res.write(String(coronavirus_stats));
        res.end()
    }

    getCoronaVirusStatus(coronaVirusStats);
}).listen(8080); //the server object listens on port 8080
