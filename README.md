# facebook-related
Facebook Related Work, most for test and data fetch

### facebook-ads-sdk-example

    related example of Facebook Ads Python SDK call, based on campaign/adset/ad/creative/insight
    
### facebook-success-creatives

    crawl https://www.facebook.com/business/success/ and get creatives inside it, written by nodejs, only for play

### facebook-fan-page-fetcher

    It's written with CasperJS and used as Facebook fan-page fetcher, only for study use.
    
    # set configuration.js
    start_url : url related with Fan Page ID likers.
    email: you need to log in before do crawler, so put a valid email here.
    pass: you need to log in before do crawler, so put password related with email.
    wait_time_unit: set wait_time between each "scroll to bottom" action, 1000 as 1000ms
    max_loop_num: set how many time of "scroll to bottom" action to do
    
    # warning
    Facebook may put email into black list if it's executed too many times, I add a random factor to protect that, but still please don't set max_loop_num to a too large number, it's unfriendly.
    
    #usage
    casperjs bin/fan_page_fetcher.js 
    data could be found in output/ folder
