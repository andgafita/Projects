<?php if(!isset($_SESSION))session_start();
//require_once '../core/DB.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Home</title>
    <!--<link rel="stylesheet" type="text/css" media="screen" href="style.css" />-->

</head>

<body>
    <div id="wrapper">
        <nav>
        <button onclick="location.href='/mvc/public/home';">Home</button>
            <button onclick="location.href='/mvc/public/accountsettings';">Account settings</button>
            <button onclick="location.href='/mvc/public/badges';">Badges</button>
            <button onclick="location.href='/mvc/public/yomovies';" class="currentButton">YoMovies</button>
            <button onclick="location.href='/mvc/public/addcontroller';">Upload</button>
        </nav>

        <div id="vidlist" style="margin-top:50px">
                <?php

            function getUserByID($id){
                $con = DB::getInstance()->getConnection();
                $stmt = $con->prepare('SELECT username FROM users WHERE id=?');
                $stmt->bindParam(1, $id, PDO::PARAM_INT);
                $stmt->execute();
                $row = $stmt->fetch(PDO::FETCH_ASSOC);
        
                return $row['username'];
            }

            foreach($data as $movie)
                if($movie->title!="")echo '<a style="text-decoration:none" href="/mvc/public/uploadcontroller/upload/' . $movie->clip_id . '">
                    <article>
                        <img src="/mvc/app/contents/thumbnails/' . $movie->thumbnail_path . '" alt="video photo">
                        <section>
                            <h3>' . $movie->title . '</h3>
                            <p>' . $movie->description . '</p>
                            <br>
                            <p>Rating: ' . $movie->rating . ' with ' . $movie->votes . ' votes.</p>
                            <br>
                            <h4>Uploaded by ' . getUserByID($movie->uploader_id) . '</h4>
                            <h4>Uploaded on ' . $movie->upload_date.'</h4>
                            <h4>Views: ' . $movie->views . '</h4>
                        </section>
                    </article>
                </a>';
                
        ?>
        </div>
    </div>
    <style><?php include __DIR__ . "/../../../public/css/style.css"; ?></style>
</body>
</html>
