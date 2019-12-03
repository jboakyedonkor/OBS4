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
   
//     var token = JSON.parse(localStorage.getItem('token'));
//     console.log(`Authorization=Bearer ${token.token}`)
//     let data = {
//       'amount':1299
//   }
//     fetch('http://localhost:5001/aapl/share_price' )
//         .then(res => res.json())
//         .then(data => {
//           document.getElementById("aapl-price").innerHTML += data.Price;
//             console.log(data.Price)
            
//         })
//         .catch(err => { console.log(err) })
// }