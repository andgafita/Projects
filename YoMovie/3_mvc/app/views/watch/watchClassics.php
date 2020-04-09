<!DOCTYPE <!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Home</title>
</head>

<body>
    <div id="wrapper">

        <nav>
        <button onclick="location.href='/mvc/public/home';">Home</button>
            <button onclick="location.href='/mvc/public/classicmovies';">Classic movies</button>
            <button onclick="location.href='/mvc/public/accountsettings';">Profile</button>
            <button onclick="location.href='/mvc/public/addcontroller'">Upload</button>
            <button onclick="location.href='/mvc/public/logincontroller';"><?php if(!isset($_SESSION['user']))echo 'Login/Sign up'; else echo 'Logout';?></button>
        </nav>

        <div id="videoPageMainContent">
        <br>
        <video width="90%" height="500px" id="videoElement" controls autoplay>
            <?php 

                echo '<source src="/mvc/app/contents/uploads/' . $model->clipPath . '" id="sursaVid" type="video/mp4">
                 </video>';
            ?>


        </div>
    </div>


    <script>

        document.getElementById('videoElement').onended = function() {
            var xhr = new XMLHttpRequest(); 
            xhr.open('POST', '/mvc/app/controllers/getBestClip.php', true);
            var formData = new FormData();
            formData.append('idChoice',<?php echo $model->id;?>);
            xhr.onload = function () {
                if(xhr.readyState == 4) {
                if (xhr.status === 200) {
                    redirectChoiceWatch(xhr.responseText);
                   }
                } else {
                    alert('An error occurred!');
                }
                }
            xhr.send(formData);
        }


        function redirectChoiceWatch(idChoice) {
            let choiceForm = document.createElement('form');
            choiceForm.setAttribute('action',"/mvc/public/watchclassics/watch/" + idChoice);
            choiceForm.setAttribute('method','POST');
            document.body.appendChild(choiceForm);
            choiceForm.submit();
        }

    </script>
</body>


<style>
    <?php include __DIR__ . '/../../../public/css/style.css';?>
    </style>
</html>
