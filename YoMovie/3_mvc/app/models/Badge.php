<?php
class Badge extends Model {
    public $id = 0;
    public $iconPath = '';
    public $title = '';
    public $description = '';
    public $movieId = 0;
    
    public function __construct($idBadge) {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT * FROM badges WHERE id=?');
        $stmt->bindParam(1, $idBadge, PDO::PARAM_INT);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if($row) {
           $this->id = $row['id'];
           $this->description = $row['description'];
           $this->title = $row['title'];
           $this->iconPath = $row['icon_path'];
           $this->movieId = $row['movie_id'];
        }
        
    }

    public static function getUserBadges($pair,$idMovie) {
        $badges = [];
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT DISTINCT choices.movie_id FROM users JOIN rewards ON
        users.id=rewards.user_id JOIN badges ON badges.id=rewards.badge_id 
        JOIN choices ON choices.badge_id=badges.id WHERE users.id=? AND choices.movie_id=?');
        $stmt->bindParam(1, $idUser, PDO::PARAM_INT);
        $stmt->bindParam(2, $idMovie, PDO::PARAM_INT);
        $stmt->execute();
        while($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            array_push($moviesViewed, Movie::getMovieOr404($row['movie_id']));
        }
        return $badges;
    }
} 
