// const app = window.document.getElementById('root')
// alert("yeeeer");




var request = new XMLHttpRequest()
request.open('GET', 'http://127.0.0.1:5001/aapl/share_price', true)
request.onload = function() {
  // Begin accessing JSON data here
  var data = JSON.parse(this.response)
 console.log(data)
}

request.send()