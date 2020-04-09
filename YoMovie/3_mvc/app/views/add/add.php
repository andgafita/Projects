<?php header('Content-Type: text/html'); ?>
<?php 
    if (!isset($_SESSION)) session_start(); 
    if (!isset($_SESSION['user'])) header("Location: /mvc/public/logincontroller");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Home</title>

    <style>
        <?php include __DIR__ . '/../../../public/css/style.css';?>/
    </style>

    <?php
        if(array_key_exists('wrongForm', $data)) {
            echo '
            <script>
            document.addEventListener(\'DOMContentLoaded\', run => {
                document.getElementById(\'wrongForm\').innerHTML = "' . $data['wrongForm'] . '";
                }
            );
            </script>
            ';
        }
    ?>

    <script>
        var count = 0;

        function addActor()
        {
            var form = document.getElementById('movieData');
            var addButton = document.getElementById('addButton');

            var br = document.createElement("br");
            form.insertBefore(br, addButton);

            var titlu = document.createElement("h1");
            var node = document.createTextNode("Actor " + ++count);
            titlu.appendChild(node);
            form.insertBefore(titlu, addButton);

            var numeAnnotation = document.createElement("p");
            var node = document.createTextNode("Nume:");
            numeAnnotation.appendChild(node);
            form.insertBefore(numeAnnotation, addButton);
            
            var nume = document.createElement("input");
            nume.type = "text";
            nume.name = "nume" + count;
            form.insertBefore(nume, addButton);

            var prenumeAnnotation = document.createElement("p");
            var node = document.createTextNode("Prenume:");
            prenumeAnnotation.appendChild(node);
            form.insertBefore(prenumeAnnotation, addButton);
            
            var prenume = document.createElement("input");
            prenume.type = "text";
            prenume.name = "prenume" + count;
            form.insertBefore(prenume, addButton);

            var varstaAnnotation = document.createElement("p");
            var node = document.createTextNode("Varsta:");
            varstaAnnotation.appendChild(node);
            form.insertBefore(varstaAnnotation, addButton);
            
            var varsta = document.createElement("input");
            varsta.type = "text";
            varsta.name = "varsta" + count;
            form.insertBefore(varsta, addButton);

            var br = document.createElement("br");
            form.insertBefore(br, addButton);

            document.getElementById('count').value = count;
        }
    
    </script>

</head>

<body>
    <div id="wrapper">
        <nav>
                <button onclick="location.href='/mvc/public/home';">Home</button>
                <button onclick="location.href='/mvc/public/classicmovies';">Classic movies</button>
                <button onclick="location.href='/mvc/public/accountsettings';">Profile</button>
                <button onclick="location.href='/mvc/public/addcontroller'" id="currentButton">Upload</button>
                <button onclick="location.href='/mvc/public/logincontroller';">Logout</button>
        </nav>

        <div id="loginPageContent">
            <div id="leftSide"></div>
            <div id="middlePart">

                    <form name="movieData", id="movieData", action="/mvc/public/addController/add", method="POST", enctype="multipart/form-data">
                            <h1>Add movie</h1> 
                            <p id="wrongForm"></p>
                            <p>Title:</p>
                            <input type="text" name="title" required>
                            <p>Description:</p>
                            <input type="text" name="description" required>
                            <p>Genre:</p>
                            <select name="genre" required>
                                <option value="Action">Action</option>
                                <option value="Comedy">Comedy</option>
                                <option value="Drama">Drama</option>
                                <option value="Horror">Horror</option>
                            </select>
                            <p>Thumbnail:</p>
                            <input type="file" style="all:initial" name="thumbnail" required>
                            <br><button id="addButton" onclick="addActor()" type="button">Actor (+)</button>
                            <input type="hidden" id="count" name="count" value="">
                            <br><button id="submitButton" type="submit" form="movieData" value="Submit">Submit</button>
                        </form>
            </div>
            <div id="rightSide"></div>
        </div>


    </div>
</body>
</html>
