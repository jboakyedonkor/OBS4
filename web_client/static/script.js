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


            var delayInMilliseconds = 50;

    setTimeout(function() {
          location.reload(true);
          parent.window.location.reload(true);
          window.location.reload(true);

    }, delayInMilliseconds);
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
});
}





function submit_account() {

  var newAccount = document.getElementById("newAccount");

  console.log(newAccount.value);

  var entry = {
      newAccount: newAccount.value,
   };

  fetch(`${window.origin}/addAccount`, {
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

      var delayInMilliseconds = 50;

    setTimeout(function() {
          location.reload(true);
          parent.window.location.reload(true);
          window.location.reload(true);

    }, delayInMilliseconds);
        });

  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
});
}


function submit_purchase(val) {

  var buyAmount = document.getElementById(val+"ShareAmount");
  var Symbol = val.toLowerCase();


  var entry = {
      Symbol: Symbol,
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


            var delayInMilliseconds = 50;

    setTimeout(function() {
          location.reload(true);
          parent.window.location.reload(true);
          window.location.reload(true);

    }, delayInMilliseconds);
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
});
}

function submit_sell(val) {

  var sellAmount = document.getElementById(val+"ShareAmount");
  var Symbol = val.toLowerCase();


  var entry = {
      Symbol: Symbol,
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


            var delayInMilliseconds = 50;

    setTimeout(function() {
          location.reload(true);
          parent.window.location.reload(true);
          window.location.reload(true);

    }, delayInMilliseconds);
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
});
}







function passSymbol(sym) {


	 var getSym= sym;


  var entry = {
      getSym: getSym.value,

  };

    fetch(`${window.origin}/getSym`, {
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

            var delayInMilliseconds = 50;

    setTimeout(function() {
          location.reload(true);
          parent.window.location.reload(true);
          window.location.reload(true);

    }, delayInMilliseconds);
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
});


}


function dropFunction() {

    var e = document.getElementById("userInfo");
	var result = e.options[e.selectedIndex].text;

    fetch(`${window.origin}/getUser`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(result),
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

            var delayInMilliseconds = 50;

    setTimeout(function() {
          location.reload(true);
          parent.window.location.reload(true);
          window.location.reload(true);

    }, delayInMilliseconds);
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
