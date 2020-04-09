<?php header('Content-Type: text/html'); //echo getcwd();?>
<?php 
    session_start(); 
    if(!isset($_SESSION['user']))header("Location: /mvc/public/logincontroller");
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Account Settings</title>
        
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
        <nav>
            <button onclick="location.href='/mvc/public/home';">Home</button>
            <button onclick="location.href='/mvc/public/accountsettings';" class="currentButton">Account settings</button>
            <button onclick="location.href='/mvc/public/badges';" >Badges</button>
            <button onclick="location.href='/mvc/public/yomovies';">YoMovies</button>
            <button onclick="location.href='/mvc/public/addcontroller';">Upload</button>
    </nav>
       <section id="container-2">
           <div id="left-side" class="side"></div>
           <div id="middle-side">
            <form class="dateCont", action="/mvc/public/accountSettings/updateData", method="POST">
                <img src="../app/views/accountSettings/avatar.png" alt="Avatar">
                <p>Username:</p>
                <input type="text", name="username", onblur="javascript:signalUsernameExists (this.value, '')", value=<?php echo $_SESSION['user'];?> >
                <span class="hiddenUsername" id="errUsernameCheck"><br><br>Username already exists, pick another one...</span>
                <br>
                <p>Email:</p>
                <input type="text", name="email", onblur="javascript:signalEmailExists (this.value, '')", value=<?php getMail(); ?> >
                <span class="hiddenEmail" id="errEmailCheck"><br><br>Email already registered!</span>
                <br>
                <p>New password:</p>
                <input type="password" name="newPass">
                <p>Confirm new password:</p>
                <input type="password" name="confNewPass">
                <br>
                <input type="submit" class="profileButtons" id="saveChangesButton" value="Save changes">
                <button type="reset" class="profileButtons"  value="Delete account">Delete account</button>
            </form> </div>
           <div id="right-side" class="side"></div>
        </section>

        <?php
            function getMail(){
                $con = DB::getInstance()->getConnection();
                $stmt = $con->prepare('SELECT email FROM users WHERE username=?');
                $stmt->bindParam(1, $_SESSION['user'], PDO::PARAM_STR,20);
                $stmt->execute();
                $row = $stmt->fetch(PDO::FETCH_ASSOC);

                echo $row['email'];
            }
        ?>

        <style><?php include __DIR__ . "/../../../public/css/stylesheet.css"; ?></style>
    </body>
</html>
