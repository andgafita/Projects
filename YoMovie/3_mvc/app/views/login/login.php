<?php header('Content-Type: text/html'); ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Home</title>
    <!--<link rel="stylesheet" href="/style.css" />-->
    <style>
        .errUsername {
        display: inline;
        color: red;
        background-color: white;
        font-family: sans-serif;
        padding-top: 5px;
        }
        .errEmail {
        display: inline;
        color: red;
        background-color: white;
        font-family: sans-serif;
        padding-top: 5px;
        }
        .hiddenUsername {
            display: none;
        }
        .hiddenEmail {
            display: none;
        }
    </style>

    <script type="text/javascript">
        var request; 

        function loadXMLUsername (url) {
        if (window.XMLHttpRequest) { 
            request = new XMLHttpRequest ();
        }
        else 
            if (window.ActiveXObject) {   
                request = new ActiveXObject ("Microsoft.XMLHTTP");
            }

        if (request) {	
            request.onreadystatechange = handleResponseUsername;
            request.open ("GET", url, true);
            request.send (null);
        } else {
            console.log ('No Ajax support :(');
        }
        }

        function handleResponseUsername () {
            if (request.readyState == 4) {
                if (request.status == 200) {
                    var response = request.responseXML.documentElement;
                    var res = response.getElementsByTagName('result')[0].firstChild.data;
                    signalUsernameExists ('a', res);
                }
                else {
                    console.log ("A problem occurred (XML data transfer):\n" +
                        response.statusText);
                }
            }
        }


        function signalUsernameExists (name, exist) {
            if(name!="")
                if (exist != '') {
                    var msg = document.getElementById ('errUsernameCheck');
                    msg.className = exist == 1 ? 'errUsername' : 'hiddenUsername';
                } else {
                    loadXMLUsername ('/mvc/app/controllers/checkExistsUsername.php?username=' + name);
                }
        }

        //Email ajax request & processing

        function loadXMLEmail (url) {
        if (window.XMLHttpRequest) { 
            request = new XMLHttpRequest ();
        }
        else 
            if (window.ActiveXObject) {   
                request = new ActiveXObject ("Microsoft.XMLHTTP");
            }

        if (request) {	
            request.onreadystatechange = handleResponseEmail;
            request.open ("GET", url, true);
            request.send (null);
        } else {
            console.log ('No Ajax support :(');
        }
        }

        function handleResponseEmail () {
            if (request.readyState == 4) {
                if (request.status == 200) {
                    var response = request.responseXML.documentElement;
                    var res = response.getElementsByTagName('result')[0].firstChild.data;
                    signalEmailExists ('a', res);
                }
                else {
                    console.log ("A problem occurred (XML data transfer):\n" +
                        response.statusText);
                }
            }
        }   


        function signalEmailExists (email, exist) {
            if(email!="")
                if (exist != '') {
                    var msg = document.getElementById ('errEmailCheck');
                    msg.className = exist == 1 ? 'errEmail' : 'hiddenEmail';
                } else {
                    loadXMLEmail ('/mvc/app/controllers/checkExistsEmail.php?email=' + email);
                }
        }
    </script>

</head>

<body>
    <div id="wrapper">
        <nav>
        <button onclick="location.href='/mvc/public/home';">Home</button>
                <button onclick="location.href='/mvc/public/classicmovies';">Classic movies</button>
                <button onclick="location.href='/mvc/public/accountsettings';">Profile</button>
                <button onclick="location.href='/mvc/public/addcontroller'">Upload</button>
                <button id="currentButton" onclick="location.href='/mvc/public/logincontroller';"><?php if(!isset($_SESSION['user']))echo 'Login/Sign up'; else echo 'Logout';?></button>
        </nav>
        <div id="loginPageContent">
            <div id="leftSide"></div>
            <div id="middlePart">
                    <form name="dateLogin", id="dateLogin", action="/mvc/public/loginController/autentificare", method="POST">
                        <?php
                            if(array_key_exists('succes',$data)) {
                                echo '<h2 style="color:red;margin-bottom: 30px;">' . $data['succes'] . '</h2>';
                            }
                            else if(array_key_exists('wrongForm',$data)) {
                                echo '<h2 style="color:red;margin-bottom: 30px;">' . $data['wrongForm'] . '</h2>';
                            }
                        ?>
                        <h1>Log in</h1>
                        <p>Username:</p>
                        <input type="text" name="username">
                        <p>Password:</p>
                        <input type="password" name="pass">
                        <button>Log in</button>
                    </form>
                    <form name="dateSignup", id="dateSignup", action="/mvc/public/loginController/inregistrare", onsubmit="return verificareForm()", method="POST">
                            <h1>Sign Up</h1>
                            <p id="alertaForm"></p> 
                            <p>Email:</p>
                            <input type="text" name="email" onblur="javascript:signalEmailExists (this.value, '')" required>
                            <span class="hiddenEmail" id="errEmailCheck">Email already registered!</span>
                            <p>Username:</p>
                            <input type="text" name="username" onblur="javascript:signalUsernameExists (this.value, '')" required>
                            <span class="hiddenUsername" id="errUsernameCheck">Username already exists, pick another one...</span>
                            <p>Password:</p>
                            <input type="password" name="pass" required>
                            <p>Confirm Password:</p>
                            <input type="password" name="confirmpass" required>
                            <button type="submit" form="dateSignup" value="Submit">Sign up</button>
                        </form>
            </div>
            <div id="rightSide"></div>
        </div>


    </div>

<script>
    function verificareForm() {
        var pass = document.forms["dateSignup"]["pass"].value;
        var confPass = document.forms["dateSignup"]["confirmpass"].value;
        if(pass.localeCompare(confPass) != 0) {
            let alerta = document.getElementById('alertaForm');
            alerta.innerHTML = "Passwords don't match!";
            return false;
        }
    }
</script>
<style><?php include __DIR__ . "/../../../public/css/style.css"; ?></style>
</body>

</html>
