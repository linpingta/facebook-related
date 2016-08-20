//var http = require('http');
//
//http.createServer(function(req, res){
//	res.writeHead(200, {'Content-Type': 'text/plain'});
//	res.end('Hello World');
//}).listen(8888);

var http = require('http');
var request = require('request');
var cheerio = require('cheerio');
var fs = require('fs');

var start_url_prefix = 'https://www.facebook.com/business/success/page/';
var total_page_num = 25;
var results = []

function check_success(start_url_prefix, total_page_num, request, cheerio){

	for (var i = 2; i < total_page_num; i++){
		start_url = start_url_prefix + String(i);
		console.log('start_url ' + start_url);
		var options = {
			url: start_url,
			headers: {
				'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
			}
		};
		//request(start_url, function(error, response, body){
		request(options, function(error, response, body){
			if (!error && response.statusCode == 200){
				var $ = cheerio.load(body);
				$('div._44vw a._3cr5').each(function(i, element){
					var facebook_prefix = "https://www.facebook.com/"
					var success_story_url_part = element.attribs.href;
					var company_name = success_story_url_part.replace('business/success/', '');
					var success_story_url_all = facebook_prefix + success_story_url_part
					console.log(success_story_url_all);
					var story_options = {
						url: success_story_url_all,
						headers: {
							'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
						}
					}
					//request(success_story_url_all, function(error, response, body){
					request(story_options, function(error, response, body){
						if (!error && response.statusCode == 200){
							var $ = cheerio.load(body);						
							// for image case
							$('div._5je5._5bgk img._5je5.img').each(function(i, element){
								var image_url = element.attribs.src;
								console.log(image_url);
								var s = {'company_name':company_name, 'facebook_link':success_story_url_all, 'image_url':image_url};
								results.push({'company_name':company_name, 'facebook_link':success_story_url_all, 'image_url':image_url});
								fs.appendFile('output/results', JSON.stringify(s));
							});
							// for video case
							$('div._5bgk video._ox1').each(function(i, element){
								var video_url = element.attribs.src;
								console.log(video_url);
								var s = {'company_name':company_name, 'facebook_link':success_story_url_all, 'video_url':video_url};
								results.push({'company_name':company_name, 'facebook_link':success_story_url_all, 'video_url':video_url});
								fs.appendFile('output/results', JSON.stringify(s));
							});
						}
						else{
							console.log('error exists in ' +  success_story_url_all + ' visited');
						}
					});
				});
			}
			else{
				console.log('error exists in ' + start_url + ' fetched');
			}
		});
	}
};

check_success(start_url_prefix, total_page_num, request, cheerio);
