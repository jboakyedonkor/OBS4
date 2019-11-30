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