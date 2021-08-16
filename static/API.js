function commas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}



var APIKey = 'AIzaSyChexdcc_Ucu8qQUlFZyXDbhfiiCIFfS-A';
var Userid = 'UC0BletW9phE4xHFM44q4qKA';
var titleChannel = document.getElementById('titleChannel');
var subscriberCount = document.getElementById('subscriberCount');
var viewCount = document.getElementById('viewCount');
var videoCount = document.getElementById('videoCount');
var publishedAt = document.getElementById('publishedAt');
var lang = document.getElementById('lang');
var picChannel = document.getElementById('picChannel');

let getdata = () => {
    fetch(`https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet&id=${Userid}&key=${APIKey}`)
        .then(response => {
            return response.json()
        })
        .then(data => {
            console.log(data);
            titleChannel.innerHTML = data["items"][0].snippet.localized.title;
            subscriberCount.innerHTML = commas(data["items"][0].statistics.subscriberCount);
            viewCount.innerHTML = commas(data["items"][0].statistics.viewCount);
            videoCount.innerHTML = commas(data["items"][0].statistics.videoCount);
            publishedAt.innerHTML = data["items"][0].snippet.publishedAt;
            lang.innerHTML = data["items"][0].snippet.country;
            picChannel.innerHTML = data["items"][0].snippet.thumbnails.high.url;




        })
}

getdata();