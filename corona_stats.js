/**
 * Created by wormgear on 2020/07/11.
 */
// import modules
var util = require('util');
var http = require('http');
var https = require('https');
var url = require('url');
var events = require('events');
//var JSON = require('JSON');
const url_today = 'https://covid19-japan-web-api.now.sh/api/v1/total';
const url_yesterday = url_today + '?history=true';
const urls = [url_today, url_yesterday];
var date = undefined;
var positive = undefined;
var death = undefined;
var todaysEpochDate = Date.now();
var debug = false;


http.createServer(function (req, res) {
    var todaysDate = getDate(todaysEpochDate);
    var yesterdaysDate = String(getDate(todaysEpochDate - 86400000));
    var dayBeforeYesterdaysDate = String(getDate(todaysEpochDate - (86400000 * 2)));
    var prevCases = 0;
    var prevDeaths = 0;
    var currCases = 0;
    var currDeaths = 0;
    var newCases = 0;
    var newDeaths = 0;

    function getDate (epochSeconds, results) {
        const d = new Date(epochSeconds);
        const strDateList = d.toLocaleString().split('/');
        var curDay = strDateList[1];
        var curMonth = strDateList[0];
        const curYearList = strDateList[2];
        const curYear = curYearList.split(',')[0];
        if(curMonth < 10) {curMonth = '0' + curMonth}
        if(curDay < 10) {curDay = '0' + curDay}
        return String(curYear + curMonth + curDay);
    }

    const urls = [url_today, url_yesterday];
    urls.forEach(function (url) {
        if (debug == true) {
            console.log(url)
        }
        https.get(url, function (data) {
            data.on('data', function (d) {
                if (url.includes('history')) {
                    var beginTargetIndex = undefined;
                    var unparsedOutput = d.toString();
                    if(unparsedOutput.search(yesterdaysDate) < 0) {
                        beginTargetIndex = unparsedOutput.search(dayBeforeYesterdaysDate)
                    } else {
                        beginTargetIndex = unparsedOutput.search(yesterdaysDate)
                    }
                    if (beginTargetIndex > 0) {
                        var preparsedOutput = unparsedOutput.slice(beginTargetIndex, unparsedOutput.length);
                        var endTargetIndex = preparsedOutput.search('},');
                        var parsedOutput = '  { \"date\": ' + preparsedOutput.slice(0, endTargetIndex) + '}';
                        parsedOutput = parsedOutput.replace(']', '');
                    }
                    httpsOutput = parsedOutput;
                } else {
                    httpsOutput = d.toString();
                    if (JSON.parse(httpsOutput).date == yesterdaysDate) {
                        if (debug == true) {
                            console.log("WARNING! date == yesterdaysDate")
                        }
                        todaysDate = String(getDate(todaysEpochDate - (86400000)));
                        yesterdaysDate = String(getDate(todaysEpochDate - (86400000 * 2)));
                        dayBeforeYesterdaysDate = String(getDate(todaysEpochDate - (86400000 * 3)));
                    }
                }
                if (debug == true) {
                    console.log('httpsOutput:\n' + httpsOutput)
                }
                if (httpsOutput != undefined) {
                    var count = (httpsOutput.match(/}/g) || []).length;
                    if (debug == true) {
                        console.log('httpsOutput contains ' + count + ' occurrences of \"}\"');
                    }
                    if (count > 1) {
                        var lastChar = httpsOutput.slice(httpsOutput.length - 1, httpsOutput.length)
                        if (lastChar == '}') {
                            httpsOutput = httpsOutput.slice(0, httpsOutput.length - 2)
                        }
                    }
                    var output = JSON.parse(httpsOutput);
                    date = output.date;
                    positive = output.positive;
                    death = output.death;
                    if (date == todaysDate) {
                        if (currCases == 0) {
                            currCases = positive;
                        }
                        if (currDeaths == 0) {
                            currDeaths = death;
                        }
                    } else {
                        if (prevCases == 0) {
                            prevCases = positive;
                        }
                        if (prevDeaths == 0) {
                            prevDeaths = death;
                        }
                    }
                    if (currCases != 0 && prevCases != 0) {
                        newCases = currCases - prevCases;
                        newDeaths = String(currDeaths - prevDeaths);
                    }
                    if(newCases + newDeaths > 0) {
                        var stats = [String(newCases), String(newDeaths)];
                    }
                if (debug == true) {
                    console.log('date =\n' + date)
                    console.log('currCases =\n' + currCases)
                    console.log('currDeaths =\n' + currDeaths)
                    console.log('prevCases =\n' + prevCases)
                    console.log('prevDeaths =\n' + prevDeaths)
                    console.log('newCases =\n' + newCases)
                    console.log('newDeaths =\n' + newDeaths)
                }
                }
                if (stats != undefined) {
                    var corona_stats = (stats[0] + ', ' + stats[1]);
                    res.write(corona_stats, function(err) { res.end(); });
                }
            }).on('end', function(){});
            res.on('error', function (e) {
                console.error(e);
            });
        });
    });
}).listen(8081); //the server object listens on port 8888

