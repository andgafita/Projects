<?php

class Movie extends Model {
    public $id;
    public $clip_id;
    public $uploader_id;
    public $title;
    public $rating;
    public $votes;
    public $upload_date;
    public $thumbnail_path;
    public $genre;
    public $description;
    public $views;

    public function __construct() {
        ;
    }

    public function set($clip_id, $uploader_id, $title, $thumbnail_path, $genre, $description) {
        $this->clip_id = $clip_id;
        $this->uploader_id = $uploader_id;
        $this->title = $title;
        $this->rating = '0.00';
        $this->votes = 0;
        $this->upload_date = date("Y-m-d H:i:s", time());
        $this->thumbnail_path = $thumbnail_path;
        $this->genre = $genre;
        $this->description = $description;
        $this->views = 0;
    }

    private function getMaxMovieId()
    {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT MAX(id) as maximum FROM movies');
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        $idMax = $row['maximum'] + 1;
        return $idMax;
    }

    public static function getMovieID($title)
    {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT id FROM movies WHERE title=?');
        $stmt->bindParam(1, $title, PDO::PARAM_STR);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($row) {
            return $row['id'];
        }
        else {
            return NULL;
        }
    }

    public static function getMovieOr404($id) {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT * FROM movies WHERE id=?');
        $stmt->bindParam(1, $id, PDO::PARAM_INT);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($row) {
           $movie = new Movie();
           $movie->id = $row['id'];
           $movie->clip_id = $row['clip_id'];
           $movie->uploader_id = $row['uploader_id'];
           $movie->title = $row['title'];
           $movie->rating = $row['rating'];
           $movie->votes = $row['votes'];
           $movie->upload_date = $row['upload_date'];
           $movie->thumbnail_path = $row['thumbnail_path'];
           $movie->genre = $row['genre'];
           $movie->description = $row['description'];
           $movie->views = $row['views'];
           return $movie;
        }	
        else {
            return NULL;
        }
    }

    public function commit() {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT * FROM movies WHERE id=?');
        $stmt->bindParam(1, $this->id, PDO::PARAM_INT);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if($row) {
            $stmt = $con->prepare('UPDATE movies SET clip_id=?, uploader_id=?, title=?, rating=?, votes=?, upload_date=?, thumbnail_path=?, genre=?, description=?, views=? WHERE id=?');
            $stmt->bindParam(1, $this->clip_id, PDO::PARAM_INT);
            $stmt->bindParam(2, $this->uploader_id, PDO::PARAM_INT);
            $stmt->bindParam(3, $this->title, PDO::PARAM_STR);
            $stmt->bindParam(4, $this->rating, PDO::PARAM_STR);
            $stmt->bindParam(5, $this->votes, PDO::PARAM_INT);
            $stmt->bindParam(6, $this->upload_date, PDO::PARAM_STR);
            $stmt->bindParam(7, $this->thumbnail_path, PDO::PARAM_STR);
            $stmt->bindParam(8, $this->genre, PDO::PARAM_STR);
            $stmt->bindParam(9, $this->description, PDO::PARAM_STR);
            $stmt->bindParam(10, $this->views, PDO::PARAM_INT);
            $stmt->bindParam(11, $this->id, PDO::PARAM_INT);
            $stmt->execute();
        }
        else {
            $this->id = $this->getMaxMovieId();
            $stmt = $con->prepare('INSERT INTO movies (id, clip_id, uploader_id, title, rating, votes, upload_date, thumbnail_path, genre, description, views) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
            $stmt->bindParam(1, $this->id, PDO::PARAM_INT);
            $stmt->bindParam(2, $this->clip_id, PDO::PARAM_INT);
            $stmt->bindParam(3, $this->uploader_id, PDO::PARAM_INT);
            $stmt->bindParam(4, $this->title, PDO::PARAM_STR);
            $stmt->bindParam(5, $this->rating, PDO::PARAM_STR);
            $stmt->bindParam(6, $this->votes, PDO::PARAM_INT);
            $stmt->bindParam(7, $this->upload_date, PDO::PARAM_STR);
            $stmt->bindParam(8, $this->thumbnail_path, PDO::PARAM_STR);
            $stmt->bindParam(9, $this->genre, PDO::PARAM_STR);
            $stmt->bindParam(10, $this->description, PDO::PARAM_STR);
            $stmt->bindParam(11, $this->views, PDO::PARAM_INT);
            $stmt->execute();
        }
    }

    public static function giveRating($id, $score) {
        $movie = Movie::getMovieOr404($id);
        if ($movie) {
            $movie->rating = (string)(((floatval($movie->rating) * $movie->votes) + $score) / ($movie->votes + 1));
            $movie->votes = $movie->votes + 1;
            $movie->commit();
        }
    }

    public static function giveView($id) {
        $movie = Movie::getMovieOr404($id);
        if ($movie) {
            $movie->views = $movie->views + 1;
            $movie->commit();
        }
    }

    public static function getViewedByUser($idUser) {
        $movies = [];
        $badges = [];
        $viz = [];
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT DISTINCT choices.movie_id, badges.id FROM users JOIN rewards ON
        users.id=rewards.user_id JOIN badges ON badges.id=rewards.badge_id 
        JOIN choices ON choices.badge_id=badges.id WHERE users.id=?');
        $stmt->bindParam(1, $idUser, PDO::PARAM_INT);
        $stmt->execute();
        while($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $movie_id = $row['movie_id'];
            $badge_id = $row['id'];
            if (!isset($viz[$movie_id]))
            {
                $viz[$movie_id] = 1;
                $movie = Movie::getMovieOr404($movie_id);
                array_push($movies, $movie);
            }
            if (!isset($badges[$movie_id])) $badges[$movie_id] = array();
            array_push($badges[$movie_id], new Badge($badge_id));
        }
        $result = ['movies' => $movies, 'badges' => $badges];
        return $result;
    }

}