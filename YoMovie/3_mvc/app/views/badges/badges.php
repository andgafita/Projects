<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Badges</title>
    </head>

    <body>
            <nav>
                <button onclick="location.href='/mvc/public/home';">Home</button>
                <button onclick="location.href='/mvc/public/accountsettings';">Account settings</button>
                <button onclick="location.href='/mvc/public/badges';" class="currentButton">Badges</button>
                <button onclick="location.href='/mvc/public/yomovies';">YoMovies</button>
                <button onclick="location.href='/mvc/public/addcontroller';">Upload</button>
            </nav>
       <section id="container-2">
           <div id="left-side" class="side">
               <p>Movies you've watched</p>
               <ul>
               <li onclick="redirectBadges(0)">All badges</li>
               <?php 

                   foreach($data['movies'] as $movie) {
                       echo '<li onclick="redirectBadges(' . $movie->id . ')" >' . $movie->title . '</li>';
                   }
                ?>
                </ul>
           </div>
           <div id="middle-side">
           <?php 
           if($data['all'] == true) {
                foreach($data['movies'] as $movie)
                foreach($data['badges'][$movie->id] as $badge) {
                   echo '<img onclick="seteazaIcon(\'' . $badge->title . '\',\'' . $badge->description . '\',\'' . $badge->iconPath . '\');" src="/mvc/app/contents/icons/' . $badge->iconPath . '" alt="insigna" class="badge">';
            }
           }
           else {
               foreach($data['badges'] as $badge) {
                echo '<img onclick="seteazaIcon(\'' . $badge->title . '\',\'' . $badge->description . '\',\'' . $badge->iconPath . '\');" src="/mvc/app/contents/icons/' . $badge->iconPath . '" alt="insigna" class="badge">';
               }
           }
         ?> 
           </div>
           <div id="right-side" class="side">
               <div id="badgeInformation" hidden>
                <img id="badgeImage" src="natureIcon.png" alt="insigna">
                <h2 id="badgeTitle"></h2>
                <p id="badgeDescription"></p>
               </div>
           </div>
        </section>

                      
    <script>

        var badgeImage = document.getElementById('badgeImage');
        var badgeTitle = document.getElementById('badgeTitle');
        var badgeDescription = document.getElementById('badgeDescription');
        var badge = document.getElementById('badgeInformation');

        function seteazaIcon(title,description,iconPath) {
            badgeTitle.innerHTML = title;
            badgeDescription.innerHTML = description;
            badgeImage.setAttribute('src',"/mvc/app/contents/icons/" + iconPath);

            badge.removeAttribute('hidden');

        }

        function redirectBadges(el) {
            window.location.href="/mvc/public/badges/" + el;
            //console.log(el);
        }
        
    </script>

        <style>
    <?php include __DIR__ . '/../../../public/css/badges.css';?>
    </style>

    </body>
</html>
