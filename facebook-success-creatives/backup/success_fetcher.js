var casper = require('casper').create({
    pageSettings: {
        loadImages: false,//The script is much faster when this field is set to false
        loadPlugins: false,
	webSecurityEnabled: false,
        //userAgent: 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
	userAgent: 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
    }
});
 
//Read configuration
var configuration = require("configuration.js");
var start_url_prefix = configuration.start_url_prefix;
var email = configuration.email;
var pass = configuration.pass;
var wait_time_unit = configuration.wait_time_unit;
var max_loop_num = configuration.max_loop_num;
 
//First step is to open Facebook
casper.start("https://facebook.com", function() {
    console.log("Facebook website opened");
});
 
//Now we have to populate username and password, and submit the form
console.log("Login using username and password");
casper.thenEvaluate(function(email, pass){
	// account may be forbidden by Facebook
        document.getElementById("email").value=email;
	document.getElementById("pass").value=pass;
	document.getElementById("loginbutton").children[0].click();
    }, {email:email, pass:pass});

var start_url = start_url_prefix + String(2);
casper.thenOpen(start_url, function(){
    console.log(start_url, ' opened');
});

casper.then(function(){
    this.download(start_url, 'result_data.html');
    this.capture('output/result_data.png');
});

//var total_page_num = 3;
//for (var i = 2; i < total_page_num; i++){
//    var start_url = start_url_prefix + String(i);
//    casper.open(start_url).then(function(){
//	console.log(start_url, ' opened');
//    });
//    casper.then(function(){
//	var store_png = 'output/result_data' + String(i) + '.png';
//        this.capture(store_png);
//    });
//}

casper.run();
