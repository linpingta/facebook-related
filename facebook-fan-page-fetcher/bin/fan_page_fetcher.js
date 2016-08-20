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
var configuration = require("../configuration.js");
var start_url = configuration.start_url;
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

casper.thenOpen(start_url, function(){
    console.log(start_url, ' opened');
});

var loop_idx = 1
casper.repeat(max_loop_num, function(){
    var wait_time = wait_time_unit + Math.ceil(Math.random() * wait_time_unit / 2);
    this.echo(loop_idx);
    loop_idx++;
    this.scrollToBottom();
    this.wait(wait_time);
});

casper.then(function(){
    this.capture('output/result_data.png');
});

casper.waitForSelector('a[href^="https://www.facebook.com/"][href$="ref=br_rs"]', function(){
    var fan_users = this.getElementsAttribute('a[href^="https://www.facebook.com/"][href$="ref=br_rs"]', 'href');
    require('fs').write('output/fan_user.csv', fan_users, 'w');
    if (fan_users.length < 0){
	this.echo('fan_users empty');
    }
    else{
	this.echo('fan_users');
	for (var i=0; i < fan_users.length; i++){
	    this.echo('iter' + i + ': ' + fan_users[i]);
	}
    }
}, function timeout(){
    this.echo('wait for user info, timeout');
}, 10000);

casper.run();
