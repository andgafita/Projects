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
    <script>
        function giveView(id) {
            var xhr = new XMLHttpRequest(); 
            xhr.open('POST', '/mvc/app/controllers/giveView.php', true);
            var formData = new FormData();
            formData.append('id', id);
            xhr.send(formData);
        }
    </script>
</head>

<body>
    <div id="wrapper">
        <nav>
                <button onclick="location.href='/mvc/public/home';">Home</button>
                <button onclick="location.href='/mvc/public/classicmovies';"  id="currentButton">Classic movies</button>
                <button onclick="location.href='/mvc/public/accountsettings';">Profile</button>
                <button onclick="location.href='/mvc/public/addcontroller'">Upload</button>
                <button id="loginButton" onclick="location.href='/mvc/public/logincontroller';"><?php if(!isset($_SESSION['user']))echo 'Login/Sign up'; else echo 'Logout';?></button>
        </nav>

        <div id="searchPosition">
            <form id="searchMenu">
                <input id="searchBar" type="text"/>
                <input id="submitButton" type="button" value="Search" onclick="applyFilters()"/> <!-- type="submit" -->
            </form>
        </div>

        <div id="filterSearch">
                <section class="sortezChestii">
                    <h1>Sort by</h1>
                    <hr>
                    <button class="filterButton" onclick="getSortBy(this)">Views</button>
                    <button class="filterButton" onclick="getSortBy(this)">Trending</button>
                    <button class="filterButton" onclick="getSortBy(this)">Upload date</button>
                    <button class="filterButton" onclick="getSortBy(this)">Rating</button>
                </section>
                <section>
                <h1>Genre</h1>
                <hr>
                <button class="filterButton" onclick="getGenre(this)">Action</button>
                <button class="filterButton" onclick="getGenre(this)">Comedy</button>
                <button class="filterButton" onclick="getGenre(this)">Drama</button>
                <button class="filterButton" onclick="getGenre(this)">Horror</button>
            </section>
            <section>
                <h1>Decisions</h1>
                <hr>
                <button class="filterButton" onclick="getDecisions(this)">Few</button>
                <button class="filterButton" onclick="getDecisions(this)">Many</button>
            </section>
            <!--
            <section>
                    <h1>Length</h1>
                    <hr>
                    <button class="filterButton" onclick="getLength(this)">10 minutes</button>
                    <button class="filterButton" onclick="getLength(this)">20 minutes</button>
                    <button class="filterButton" onclick="getLength(this)">30 minutes</button>
                    <button class="filterButton" onclick="getLength(this)">40+ minutes</button>
            </section>
            -->
            <section>
                    <h1>Actor</h1>
                    <hr>
                    <input id="actorText" type="text">
            </section>
        </div>

        <div id="vidlist">
            
        <!-- <a style="text-decoration:none" href="https://www.google.com">
            <article>
                <img src="../app/views/testhome/bander.jpg" alt="video photo">
                <section>
                    <h3>This is a long videotitle and it shouldn't show all of it</h3>
                    <p>This is a really long description and it basically says nothing at all but whatever, this is here just for testing purposes and whatnot
                        so here goes the test bam bam chika wow wowThis is a really long description and it basically says nothing at all but whatever, this is here just for testing purposes and whatnot
                        so here goes the test bam bam chika wow wowThis is a really long description and it basically says nothing at all but whatever, this is here just for testing purposes and whatnot
                        so here goes the test bam bam chika wow wow
                    </p>
                </section>
            </article>
        </a> -->
        
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
                if($movie->title!="")echo '<a style="text-decoration:none" onclick="giveView(' . $movie->id . ')" href="/mvc/public/watchClassics/watch/' . $movie->clip_id . '">
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
    <script type="text/javascript">
        var sort_by="";
        var genre="";
        var decisions="";
        //var length="";
        var actor="";

        function getSortBy(element){
            if(sort_by!=""){
                document.getElementsByClassName("selectedSortby")[0].className = "filterButton";
            }
            element.className = "selectedSortby";

            sort_by = element.innerHTML; 
        }
        
        function getGenre(element){
            if(genre!=""){
                document.getElementsByClassName("selectedGenre")[0].className = "filterButton";
            }
            element.className = "selectedGenre";

            genre = element.innerHTML;
        }

        function getDecisions(element){
            if(decisions!=""){
                document.getElementsByClassName("selectedDecisions")[0].className = "filterButton";
            }
            element.className = "selectedDecisions";

            decisions = element.innerHTML;
        }

        /*function getLength(element){
            if(length!=""){
                document.getElementsByClassName("selectedLength")[0].className = "filterButton";
            }
            element.className = "selectedLength";

            length = element.innerHTML;
        }*/

        function getActor(){
            return document.getElementById("actorText").value;
        }

        function getSearch(){
            return document.getElementById("searchBar").value;
        }

        function applyFilters(){
            console.log(sort_by);
            console.log(genre);
            console.log(decisions);
            console.log(getActor());
            console.log(getSearch());

            window.location.href = "/mvc/public/home/test?" + "sort_by=" + sort_by + "&genre=" + genre + "&decisions=" + decisions + "&actor="+getActor() + "&search=" + getSearch();
        }
    </script>
    <style><?php include __DIR__ . "/../../../public/css/style.css"; ?></style>
    
</body>

</html>
