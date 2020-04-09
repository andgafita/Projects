<?php
class yomovies extends Controller {
    public function index() {
        $dataInput = $this->getUploaded();
        $this->view('yomovies/yomovies', $dataInput);
    }

    public function getUploaded(){
        if(!isset($_SESSION))session_start();
        $this->model('Movie');
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT id FROM movies WHERE uploader_id=?');
        $stmt->bindParam(1, $_SESSION['userID'], PDO::PARAM_INT);
        $stmt->execute();

        $listaFilme = array();
        while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
            $movie = Movie::getMovieOr404($row['id']);
            array_push($listaFilme, $movie);
        }

        return $listaFilme;
    }
}
