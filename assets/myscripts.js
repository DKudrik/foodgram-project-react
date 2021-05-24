let submit_button = document.getElementById("id_submit_button");

function IsEmpty() {
    email_length = document.getElementById("id_email").value.length;
    if (email_length == "") {
      alert("empty");
    }
    return;
  }

submit_button.addEventListener("mouseenter", IsEmpty);

console.log(submit_button);