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
        <video width="90%" height="500px" id="videoElement" controls>
            <?php 

                echo '<source src="/mvc/app/contents/uploads/' . $model->clipPath . '" id="sursaVid" type="video/mp4">
                 </video>';
            ?>
            <p id="intrebare" hidden="false"><?php echo $model->textIntrebare;?></p>
            <section id="videoChoiceButtons">
            <?php
            $last = 0;
            foreach ($data['childNodes'] as $choice) {
                for($i = $last + 1;$i < $choice->choiceNumber; $i++ ) {
                    echo '<button id="choice' . $i . '" hidden="true"></button>';
                }
                echo '<button id="choice' . $choice->choiceNumber . '" title="' . $choice->id . '" hidden="true">' . $choice->descriere . '</button>';
                $last = $choice->choiceNumber;
            }
            for($i = $last + 1;$i < 6;$i++) {
                echo '<button id="choice' . $i . '" hidden="true"></button>';
            }
            ?>
            </section>

            <script>
            function Rate(id)
            {
                let value = document.getElementById("rating").value;
                var xhr = new XMLHttpRequest(); 
                xhr.open('POST', '/mvc/app/controllers/giveRating.php', true);
                var formData = new FormData();
                formData.append('id', id);
                formData.append('value', value);
                xhr.send(formData);
            }
            </script>
            <?php
            Choice::giveVizualizare($model->id);
            if (empty($data['childNodes']))
            echo '
                <select id="rating" style="border:0px">
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                </select>
                <button class="filterButton" onclick="Rate(' . $model->movieId . ');">Rate</button>';
            ?>

        </div>
    </div>

    <?php 
    if($data['badge']->id != 0 && $data['added'] == 1) {
    echo '<div class="bg-model">
            <div class="modal-content">
            <p><strong>You got a new badge!</strong></p>
            <div id="badgeInformation">';
             echo '<img height="100px" width="100px" src="/mvc/app/contents/icons/' . $data['badge']->iconPath . '">';
             echo '<h2>' . $data['badge']->title . '</h2>
                <p>' . $data['badge']->description . '</p>';
    echo        '</div>
    <button id="inchide">Thanks</button>
    </div>
    </div>';
    }
    ?>

    <script>
        var choice1 = document.getElementById('choice1');
        var choice2 = document.getElementById('choice2');
        var choice3 = document.getElementById('choice3');
        var choice4 = document.getElementById('choice4');
        var choice5 = document.getElementById('choice5');

        document.getElementById('videoElement').onended = function() {
            choice1.removeAttribute('hidden');
            choice2.removeAttribute('hidden');
            choice3.removeAttribute('hidden');
            choice4.removeAttribute('hidden');
            choice5.removeAttribute('hidden');
            let intrebare = document.getElementById('intrebare');
            if(intrebare.innerHTML != '') {
                intrebare.removeAttribute('hidden');
            }
        }

        choice1.onclick = function() {
            redirectChoiceWatch(choice1.title);
        }

        choice2.onclick = function() {
            redirectChoiceWatch(choice2.title);
        }

        choice3.onclick = function() {
            redirectChoiceWatch(choice3.title);
        }

        choice4.onclick = function() {
            redirectChoiceWatch(choice4.title);
        }

        choice5.onclick = function() {
            redirectChoiceWatch(choice5.title);
        }

        document.getElementById('inchide').onclick = function() {
            document.querySelector('.bg-model').style.display = 'none';
        }

        function redirectChoiceWatch(idChoice) {
            let choiceForm = document.createElement('form');
            choiceForm.setAttribute('action',"/mvc/public/watchController/watch/" + idChoice);
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
