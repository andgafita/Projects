<?php

class AddController extends Controller {
    public function index() {
        $this->view('add/add');
    }

    private function getMaxId($table)
    {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT MAX(id) as maximum FROM ' . $table);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        $idMax = $row['maximum'] + 1;
        return $idMax;
    }

    private function commitChoice($choice)
    {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('INSERT INTO choices (id, id_precedent, movie_id, vizualizari) VALUES(?, ?, ?, 0)');
        $stmt->bindParam(1, $choice->id, PDO::PARAM_INT);
        $stmt->bindParam(2, $choice->idPrecedent, PDO::PARAM_INT);
        $stmt->bindParam(3, $choice->movieId, PDO::PARAM_INT);
        $stmt->execute();
    }

    private function saveThumbnail($file) {
        $target_dir = "/../contents/thumbnails/";
        $target_file =  __DIR__ . $target_dir . basename($file["name"]);
        $imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));
        if($imageFileType != "png" && $imageFileType != "jpg" && $imageFileType != "jpeg" && $imageFileType != "gif") {
            return "Thumbnail is not a supported image file type.";
        }
        if ($file["size"] > 1000000) {
            return "Thumbnail is too large. (max 1MB)";
        }
        if (!move_uploaded_file($file["tmp_name"], $target_file)) {
            return "There was an error uploading the thumbnail.";
        }
        return NULL;
    }

    private function parseAndCommitActors($arr)
    {
        $actors = [];
        $n = $arr['count'];
        for ($i = 1; $i <= $n; ++$i) {
            if (!empty($arr['nume' . $i]) &&
                !empty($arr['prenume' . $i]) &&
                !empty($arr['varsta' . $i])) {
                    if (Actor::getActorID($arr['nume' . $i], $arr['prenume' . $i]) == NULL) {
                        $actor = new Actor();
                        $actor->set(
                            $arr['nume' . $i],
                            $arr['prenume' . $i],
                            $arr['varsta' . $i]
                            );
                        $actor->commit();
                    }
                    else {
                        $actor = Actor::getActorOr404(Actor::getActorID($arr['nume' . $i], $arr['prenume' . $i]));
                    }
                    array_push($actors, $actor->id);
            }
        }
        return $actors;
    }

    private function parseAndCommitDistribution($actor_ids, $movie_id) {
        foreach ($actor_ids as $id) {
            $con = DB::getInstance()->getConnection();
            $stmt = $con->prepare('INSERT INTO distribution (movie_id, actor_id) VALUES (?, ?)');
            $stmt->bindParam(1, $movie_id, PDO::PARAM_INT);
            $stmt->bindParam(2, $id, PDO::PARAM_INT);
            $stmt->execute();
        }
    }

    public function add() {
        if (!isset($_SESSION)) session_start();
        $this->model('Movie');
        $this->model('Choice');
        $this->model('Badge');
        $this->model('Actor');
        if(isset($_POST['title']) &&
           isset($_POST['description']) &&
           isset($_POST['genre']) &&
           isset($_FILES['thumbnail'])) {
            if(Movie::getMovieID($_POST['title']) != NULL) {
                $this->view('add/add', ['wrongForm' => "Movie already exists!"]);
            }
            else {
                $output = $this->saveThumbnail($_FILES['thumbnail']);
                if ($output != NULL) {
                    $this->view('add/add', ['wrongForm' => $output]);
                }
                else {
                    $movie = new Movie();
                    $movie->set(
                        $this->getMaxId("choices"),                           //clip_id
                        isset($_SESSION['userID']) ? $_SESSION['userID'] : 0, //uploader_id
                        $_POST['title'],                                      //title
                        $_FILES['thumbnail']['name'],                         //thumbnail_path
                        $_POST['genre'],                                      //genre
                        $_POST['description']                                 //description                 
                        );
                    $movie->commit();

                    $actors = $this->parseAndCommitActors($_POST);

                    $this->parseAndCommitDistribution($actors, $movie->id);

                    $choice = new Choice($movie->clip_id);
                    $choice->idPrecedent = 0;
                    $choice->movieId = $movie->id;
                    $this->commitChoice($choice);
                    $badge = new Badge($choice->badgeId);
                    $this->view('upload/upload', [ 'childNodes' => [] , 'badge' => $badge ], $choice);
                }
            }
        }
        else {
            $this->view('add/add', ['wrongForm' => "Complete all fields!"]);
        }
    }
}