/**
 * Created by wormgear on 2020/07/18.
 */

var http = require('http');
var url = 'http://localhost:8081';
var cvsStats = undefined;
var cvsData = undefined;
var LED = undefined;
var Gpio = require('onoff').Gpio; //include onoff to interact with the GPIO
var RED = new Gpio(4, 'out'); //use GPIO pin 4, and specify that it is output
var YELLOW = new Gpio(17, 'out'); //use GPIO pin 4, and specify that it is output
var GREEN = new Gpio(27, 'out'); //use GPIO pin 4, and specify that it is output

//function getData(callback) {
function getData(callback) {
    http.get(url, function (data) {
        data.on('data', function (d) {
            cvsStats = d.toString().split(',')[0];
            callback(cvsStats)
        });
    }).on('end', function () {
    });
}

function rgb() { //function to light the appropriate LED
    RED.writeSync(0);
    YELLOW.writeSync(0);
    GREEN.writeSync(0);
    getData(function(cvsData) {
        if(cvsData > 350) {
            LED = RED;
        }
        if(cvsData < 300) {
            if(cvsData >= 100) {
                LED = YELLOW;
            }
        }
        if(cvsData < 100) {
            LED = GREEN;
        }
        if (LED.readSync() === 0) {
            LED.writeSync(1); //set pin state to 1 (turn LED on)
        } else {
            LED.writeSync(0); //set pin state to 0 (turn LED off)
        }
    });
}

rgb();