function submit_funds() {

  var fundAmount = document.getElementById("fundAmount");
 

  var entry = {
      fundAmount: fundAmount.value,
 
  };

  fetch(`${window.origin}/addFunds`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  .then(function(response) {
    if (response.status !== 200) {
      console.log(`Looks like there was a problem. Status code: ${response.status}`);
      return;
    }
    response.json().then(function(data) {
      console.log(data);
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
});
}

function submit_purchase(val) {

  var buyAmount = document.getElementById(val+"ShareAmount");
 

  var entry = {
      buyAmount: buyAmount.value,
 
  };

  fetch(`${window.origin}/buy`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  .then(function(response) {
    if (response.status !== 200) {
      console.log(`Looks like there was a problem. Status code: ${response.status}`);
      return;
    }
    response.json().then(function(data) {
      console.log(data);
      var buyAmount = document.getElementById(val+"ShareAmount").value =""
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
});
}

function submit_sell(val) {

  var sellAmount = document.getElementById(val+"ShareAmount");
 

  var entry = {
      sellAmount: sellAmount.value,
 
  };

  fetch(`${window.origin}/sell`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  .then(function(response) {
    if (response.status !== 200) {
      console.log(`Looks like there was a problem. Status code: ${response.status}`);
      return;
    }
    response.json().then(function(data) {
      console.log(data);
      var sellAmount = document.getElementById(val+"ShareAmount").value =""
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
});
}


function submit_sell(val) {

  var sellAmount = document.getElementById(val+"ShareAmount");
 

  var entry = {
      sellAmount: sellAmount.value,
 
  };

  fetch(`${window.origin}/sell`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  .then(function(response) {
    if (response.status !== 200) {
      console.log(`Looks like there was a problem. Status code: ${response.status}`);
      return;
    }
    response.json().then(function(data) {
      console.log(data);
      var sellAmount = document.getElementById(val+"ShareAmount").value =""
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
});
}

// window.onload = function(){ 
// //  console.log("Loaded")
// const url = 'http://localhost:5000/dashboard';

// var token = JSON.parse(localStorage.getItem('token'))
// console.log(`Authorization=Bearer ${token.token}`)
// var xhr = new XMLHttpRequest();
// xhr.open("POST", url, true);
// xhr.setRequestHeader('Content-Type', 'application/json');
// xhr.send(JSON.stringify({ 'token': token.token}));
// }