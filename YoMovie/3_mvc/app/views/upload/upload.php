<?php 
    if (!isset($_SESSION)) session_start(); 
    if(!isset($_SESSION['user']))header("Location: /mvc/public/logincontroller");
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Upload</title>
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

        <div id="videoPageMainContent">
            <?php 
            echo '<button id="previousChoice" title="' . $model->idPrecedent . '">Go to previous decision</button>';
            if($model->idPrecedent == 0) {
                echo '<script>document.getElementById(\'previousChoice\').style.display="none";</script>';
                echo '<font color ="red" style="font-size:30px;margin-bottom:30px;">You can now upload your first clip for this movie!</font>';
            }
            
            if($model->id != 0 && $model->clipPath != null) {
                echo '<video width="90%" height="500px" controls>
                <source src="/mvc/app/contents/uploads/' . $model->clipPath . '" id="sursaVid" type="video/mp4">
            </video>';
            }
            ?>
            <form action="" method="post" enctype="multipart/form-data" id="formularClip" submit="false">
                        <h1>Question</h1>
                        <textarea rows="4" columns="50" placeholder="Specify a question for the end of this choice." id="question" ><?php if($model->textIntrebare !=null) echo $model->textIntrebare; ?></textarea>
                        <h1>Select clip to upload:</h1>
                        <input type="file" id="fileToUpload">
                        <h1>Badge information</h1>
                        <textarea  id="badgeTitle" placeholder="Specify a title for this badge." ><?php if($data['badge']->title != null) echo $data['badge']->title; ?></textarea>
                        <textarea  id="badgeDescription" placeholder="Specify a description for this badge." ><?php if($data['badge']->description != null) echo $data['badge']->description; ?></textarea>
                        <input type="file" id="badgeIcon">
                        
            </form>
            <?php
                if($data['badge']->title != '' && $data['badge']->iconPath != '') {
                    echo '<img style="width:200px" height="200px" id="idBadgeIcon" src="/mvc/app/contents/icons/' . $data['badge']->iconPath . '">';
                }

            ?>
            <button id="uploadChoice">Upload clip</button>
            <input type="text" size="50%" id="choiceText" style="
    border: 0px;
    color: white;
    border-radius: 2px;
">
            <section id="videoChoiceButtons">
            <?php
            $last = 0;
            foreach ($data['childNodes'] as $choice) {
                for($i = $last + 1;$i < $choice->choiceNumber; $i++ ) {
                    echo '<button id="choice' . $i . '"></button>';
                }
                echo '<button id="choice' . $choice->choiceNumber . '" title="' . $choice->id . '">' . $choice->descriere . '</button>';
                $last = $choice->choiceNumber;
            }
            for($i = $last + 1;$i < 6;$i++) {
                echo '<button id="choice' . $i . '"></button>';
            }
            if(count($data['childNodes']) == 5) {
                echo '<button id="plus"></button>';
            }
            else {
                echo '<button id="plus">+</button>';
            }

            ?>
            </section>
        </div>


    </div>
    <script>
        var choice1 = document.getElementById('choice1');
        var choice2 = document.getElementById('choice2');
        var choice3 = document.getElementById('choice3');
        var choice4 = document.getElementById('choice4');
        var choice5 = document.getElementById('choice5');
        var plus = document.getElementById('plus');
        var choiceText = document.getElementById('choiceText');

        function getNrButtons() {
            return (choice1.innerHTML != '') +
                   (choice2.innerHTML != '') +
                   (choice3.innerHTML != '') +
                   (choice4.innerHTML != '') +
                   (choice5.innerHTML != '');
        }
        plus.addEventListener('click',e=> {
            let nrButtons = getNrButtons();
            if(nrButtons < 4) {
                if(choice1.innerHTML == '') {
                    choice1.innerHTML ='Click to set choice';
                    choice1.title = '';
                }
                else if(choice2.innerHTML == '') {
                    choice2.innerHTML ='Click to set choice';
                    choice2.title = '';
                }
                else if(choice3.innerHTML == '') {
                    choice3.innerHTML ='Click to set choice';
                    choice3.title = '';
                }
                else {
                    choice4.innerHTML ='Click to set choice';
                    choice4.title = '';
                }
            }
            else {
                document.getElementById('choice5').innerHTML = 'Click to set choice';
                choice5.title = '';
                plus.innerHTML = '';
            }
        });
        
        choice1.addEventListener('mousedown',e=> {
            if(e.button == 0) {//left click
                if(choiceText.value != '') {
                    choice1.innerHTML = choiceText.value;
                    setChoice(<?php echo $model->id; ?>, 1, choice1.innerHTML, choice1);
                }
            }
            else if(e.button == 2) {//right click
                redirectChoiceUpload(choice1.title);
            }
            else if(e.button == 1) {//middle click
                if(choice1.title != '')deleteChoice(choice1.title);
                choice1.innerHTML = '';
                plus.innerHTML = '+';
            }
        });

        choice2.addEventListener('mousedown',e=> {
            if(e.button == 0) {//left click
                if(choiceText.value != '') {
                    choice2.innerHTML = choiceText.value;
                    setChoice(<?php echo $model->id; ?>, 2, choice2.innerHTML, choice2);
                }
            }
            else if(e.button == 2) {//right click
                redirectChoiceUpload(choice2.title);
            }

            else if(e.button == 1) {//middle click
                if(choice2.title != '')deleteChoice(choice2.title);
                choice2.innerHTML = '';
                plus.innerHTML = '+';
            }
        });

        choice3.addEventListener('mousedown',e=> {
            if(e.button == 0) {//left click
                if(choiceText.value != '') {
                    choice3.innerHTML = choiceText.value;
                    setChoice(<?php echo $model->id; ?>, 3, choice3.innerHTML, choice3);
                }
            }
            else if(e.button == 2) {//right click
                redirectChoiceUpload(choice3.title);
            }

            else if(e.button == 1) {//middle click
                if(choice3.title != '')deleteChoice(choice3.title);
                choice3.innerHTML = '';
                plus.innerHTML = '+';
            }
        });

        choice4.addEventListener('mousedown',e=> {
            if(e.button == 0) {//left click
                if(choiceText.value != '') {
                    choice4.innerHTML = choiceText.value;
                    setChoice(<?php echo $model->id; ?>, 4, choice4.innerHTML, choice4);
                }
            }
            else if(e.button == 2) {//right click
                redirectChoiceUpload(choice4.title);
            }

            else if(e.button == 1) {//middle click
                if(choice4.title != '')deleteChoice(choice4.title);
                choice4.innerHTML = '';
                plus.innerHTML = '+';
            }
        });

        choice5.addEventListener('mousedown',e=> {
            if(e.button == 0) {//left click
                if(choiceText.value != '') {
                    choice5.innerHTML = choiceText.value;
                    setChoice(<?php echo $model->id; ?>, 5, choice5.innerHTML, choice5);
                }
            }
            else if(e.button == 2) {//right click
                redirectChoiceUpload(choice5.title);
            }

            else if(e.button == 1) {//middle click
                if(choice5.title != '')deleteChoice(choice5.title);
                choice5.innerHTML = '';
                plus.innerHTML = '+';
            }
        });

        function deleteChoice(idChoice) {
            var xhr = new XMLHttpRequest(); 
            xhr.open('POST', '/mvc/app/controllers/deleteChoice.php', true);
            var formData = new FormData();
            formData.append('idChoice',idChoice);
            xhr.onload = function () {
                if(xhr.readyState == 4) {
                if (xhr.status === 200) {
                    if(xhr.responseText != '') {;
                    }
                   }
                } else {
                    alert('An error occurred!');
                }
                }
            xhr.send(formData);
        }

        function setChoice(idParinte, nrChoice, choiceText, choiceButton) {
            var xhr = new XMLHttpRequest(); 
            xhr.open('POST', '/mvc/app/controllers/setChoice.php', true);
            var formData = new FormData();
            formData.append('idParinte',idParinte);
            formData.append('nrChoice',nrChoice);
            formData.append('choiceText',choiceText);
            xhr.onload = function () {
                if(xhr.readyState == 4) {
                if (xhr.status === 200) {
                    if(xhr.responseText != '') {
                        choiceButton.setAttribute('title', xhr.responseText);
                    }
                   }
                } else {
                    alert('An error occurred!');
                }
                }
            xhr.send(formData);
        }

        function redirectChoiceUpload(idChoice) {
            let choiceForm = document.createElement('form');
            choiceForm.setAttribute('action',"/mvc/public/uploadController/upload/" + idChoice);
            choiceForm.setAttribute('method','POST');
            document.body.appendChild(choiceForm);
            choiceForm.submit();

        }

        document.getElementById("previousChoice").onclick=function() {
            redirectChoiceUpload(document.getElementById('previousChoice').title);
        }

        document.getElementById('uploadChoice').onclick=function() {
            var inp = document.getElementById('fileToUpload').files;
            var intrebare = document.getElementById('question').value;
            var formData = new FormData();
            if(inp[0]!=undefined) {
                formData.append('clip',inp[0]);
            }
            formData.append('question',intrebare);
            formData.append('idClip',<?php echo $model->id; ?>);
            formData.append('badgeTitle',document.getElementById('badgeTitle').value);
            formData.append('badgeDescription',document.getElementById('badgeDescription').value);
            let badgeIcon = document.getElementById('badgeIcon').files[0];
            if(badgeIcon != undefined) {
                formData.append('badgeIcon',badgeIcon);
            }

            var xhr = new XMLHttpRequest(); 
            xhr.open('POST', '/mvc/app/controllers/fileUpload.php', true);
            xhr.onload = function () {
                if(xhr.readyState == 4) {
                if (xhr.status === 200) {

                   let idBadgeIcon = document.getElementById('idBadgeIcon');
                   let sourceVar = document.getElementById('sursaVid');
                   if(sourceVar && inp[0]!=undefined) {
                       sourceVar.setAttribute('src',"/mvc/app/contents/uploads/" + inp[0]['name']);
                   }
                   else if(inp[0] != undefined){
                       let formVar = document.getElementById('formularClip');
                       let videoNou = document.createElement("video");
                       let sursaNoua = document.createElement('source');
                       videoNou.setAttribute('height','500px');
                       videoNou.setAttribute('width','90%');
                       videoNou.setAttribute('controls',true);
                       sursaNoua.setAttribute('src',"http://localhost/mvc/app/contents/uploads/" + inp[0]['name']);
                       sursaNoua.setAttribute('id','sursaVid');
                       videoNou.appendChild(sursaNoua);
                       formVar.before(videoNou);

                   }
                   if(badgeIcon != undefined) {
                        if(idBadgeIcon) {
                            idBadgeIcon.setAttribute('src',"/mvc/app/contents/icons/" + badgeIcon['name']);
                        }
                        else {
                            let imagineNoua = document.createElement('img');
                            imagineNoua.setAttribute('height','200px');
                            imagineNoua.setAttribute('style','width:200px');
                            imagineNoua.setAttribute('id','idBadgeIcon');
                            imagineNoua.setAttribute('src',"/mvc/app/contents/icons/" + badgeIcon['name']);
                            document.getElementById('uploadChoice').before(imagineNoua);                  
                        }
                   }
                   console.log(xhr.response);
                } else {
                    alert('An error occurred!');
                }
                }
            };
            xhr.send(formData);
        }


    </script>
</body>
<style>
    <?php include __DIR__ . '/../../../public/css/style.css';?>
    </style>
</html>
