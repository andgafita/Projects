<?php
class Home extends Controller {
    public function index() {
        $dataInput = $this->getBasicList();
        $this->view('home/index', $dataInput);
    }

    public function test(){
        //echo $_GET['sort_by'];
     
        $firstQuery = false;
        $sqlCustomQuery = "SELECT id FROM movies ";

        if($_GET['genre']!=""){
            if(!$firstQuery) {$firstQuery = true;$sqlCustomQuery = $sqlCustomQuery . " WHERE ";}
                else $sqlCustomQuery = $sqlCustomQuery . " AND ";
            
            $sqlCustomQuery = $sqlCustomQuery . "genre = '" . $_GET['genre'] . "'";
        }

        if($_GET['decisions']!=""){
            if(!$firstQuery) {$firstQuery = true;$sqlCustomQuery = $sqlCustomQuery . " WHERE ";}
                else $sqlCustomQuery = $sqlCustomQuery . " AND ";
            if ($_GET['decisions'] == "Few") $prag = " < 5";
            else if ($_GET['decisions'] == "Many") $prag = " >= 5";
            $sqlCustomQuery = $sqlCustomQuery . " (SELECT COUNT(*) FROM choices WHERE (text_intrebare IS NULL OR text_intrebare = '') AND movie_id = movies.id GROUP BY movie_id)" . $prag;
        }
        
        if($_GET['actor']!=""){
            if(!$firstQuery) {$firstQuery = true;$sqlCustomQuery = $sqlCustomQuery . " WHERE ";}
                else $sqlCustomQuery = $sqlCustomQuery . " AND ";

            $sqlCustomQuery = $sqlCustomQuery . " id in (SELECT movie_id FROM distribution WHERE actor_id = (SELECT id FROM actors WHERE CONCAT(prenume, CONCAT(' ', nume)) LIKE '%" . $_GET['actor'] . "%'))";
        }
        
        if($_GET['search']!=""){
            if(!$firstQuery) {$firstQuery = true;$sqlCustomQuery = $sqlCustomQuery . " WHERE ";}
                else $sqlCustomQuery = $sqlCustomQuery . " AND ";

            $sqlCustomQuery = $sqlCustomQuery . " title LIKE '%" . $_GET['search'] . "%' ";
        }

        if($_GET['sort_by']!=""){
            if($_GET['sort_by']=="Views")$sqlCustomQuery = $sqlCustomQuery . " ORDER BY views DESC";
                else 
                    if($_GET['sort_by']=="Trending"){
                        if($firstQuery)$sqlCustomQuery = $sqlCustomQuery . " AND ";
                        else {$firstQuery = true;$sqlCustomQuery = $sqlCustomQuery . " WHERE ";}
                        $sqlCustomQuery = $sqlCustomQuery . " DATEDIFF(SYSDATE(),upload_date) <= 7 ORDER BY views DESC";
                        }
                        else if($_GET['sort_by']=="Upload date")$sqlCustomQuery = $sqlCustomQuery . " ORDER BY upload_date DESC";
                            else if($_GET['sort_by']=="Rating")$sqlCustomQuery = $sqlCustomQuery . " ORDER BY rating DESC";
        }

        //echo $sqlCustomQuery;
        
        $this->model('Movie');
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare($sqlCustomQuery);
        $stmt->execute();

        $listaFilme = array();
        while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
            $movie = Movie::getMovieOr404($row['id']);
            array_push($listaFilme, $movie);
        }

        $this->view('home/index', $listaFilme);
    }

    public function getBasicList(){
        $this->model('Movie');
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT id FROM movies');
        $stmt->execute();

        $listaFilme = array();
        while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
            $movie = Movie::getMovieOr404($row['id']);
            //$listaFilme.append($movie);
            array_push($listaFilme, $movie);
        }

        return $listaFilme;
    }
}
