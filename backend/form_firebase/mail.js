const firebaseConfig = {
  apiKey: "AIzaSyBi0T00zIXOpHaMRiDsEq2wGNtr_Mr_7Tw",
  authDomain: "cod-backend-4953e.firebaseapp.com",
  databaseURL: "https://cod-backend-4953e-default-rtdb.firebaseio.com",
  projectId: "cod-backend-4953e",
  storageBucket: "cod-backend-4953e.appspot.com",
  messagingSenderId: "1024969667436",
  appId: "1:1024969667436:web:95ff7ba57aade906797949"
};

// initialize firebase
firebase.initializeApp(firebaseConfig);

// reference your database
var contactFormDB = firebase.database().ref("form");

document.getElementById("form").addEventListener("submit", submitForm);

function submitForm(e) {
  e.preventDefault();

  var name = getElementVal("name");
  var emailid = getElementVal("emailid");
  var msgContent = getElementVal("msgContent");

  saveMessages(name, emailid, msgContent);

  //   enable alert
  document.querySelector(".alert").style.display = "block";

  //   remove the alert
  setTimeout(() => {
    document.querySelector(".alert").style.display = "none";
  }, 3000);

  //   reset the form
  document.getElementById("form").reset();
}

const saveMessages = (name, emailid, msgContent) => {
  var newContactForm = contactFormDB.push();

  newContactForm.set({
    name: name,
    emailid: emailid,
    msgContent: msgContent,
  });
};

const getElementVal = (id) => {
  return document.getElementById(id).value;
};
