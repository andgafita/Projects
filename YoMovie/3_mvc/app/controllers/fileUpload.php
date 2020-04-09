<?php
require_once '../core/DB.php';

$target_dir = "/../contents/uploads/";
$uploadOk = 1;
if(isset($_FILES["clip"])) {
$target_file = __DIR__ . $target_dir . basename($_FILES["clip"]["name"]);
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

// Check if file already exists
/*if (file_exists($target_file)) {
    echo "Sorry, file already exists.";
    //$uploadOk = 0;
}*/
// Check file size
/*if ($_FILES["fileToUpload"]["size"] > 500000) {
    echo "Sorry, your file is too large.";
    $uploadOk = 0;
}*/
// Allow certain file formats
if($imageFileType != "mp4" ) {
    echo "Sorry, only MP4 files are allowed.";
    $uploadOk = 0;
}}
// Check if $uploadOk is set to 0 by an error
$movieId = 0;

$con = DB::getInstance()->getConnection();
$stmt = $con->prepare('SELECT * FROM choices WHERE id=?');
$stmt->bindParam(1, $_POST['idClip'], PDO::PARAM_INT);
$stmt->execute();
$row = $stmt->fetch(PDO::FETCH_ASSOC);
$alreadyInserted = 0;
$badgeId = 0;
if($row) {
    $alreadyInserted = 1;
    $movieId = $row['movie_id'];
    $badgeId = $row['badge_id'];
}
if($uploadOk == 1) {
    if(isset($_FILES['clip'])) {
        if($alreadyInserted == 1) {
            $stmt = $con->prepare('UPDATE choices SET text_intrebare=?, clip_path=? WHERE id=?');
            $stmt->bindParam(1, $_POST['question'], PDO::PARAM_STR);
            $stmt->bindParam(2, $_FILES['clip']['name'], PDO::PARAM_STR);
            $stmt->bindParam(3, $_POST['idClip'], PDO::PARAM_INT);
        }
        else {
            $stmt = $con->prepare('INSERT INTO choices (id,text_intrebare,clip_path,id_precedent) VALUES(?,?,?,?)');
            $stmt->bindParam(1, $_POST['idClip'], PDO::PARAM_INT);
            $stmt->bindParam(2, $_POST['question'], PDO::PARAM_STR);
            $stmt->bindParam(3, $_FILES['clip']['name'], PDO::PARAM_STR);
            $stmt->bindValue(4, 0, PDO::PARAM_INT);
        }

        if (move_uploaded_file($_FILES["clip"]["tmp_name"], $target_file)) {
            echo "The file ". basename( $_FILES["clip"]["name"]). " has been uploaded.";
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    }
    else {
        if($alreadyInserted == 1) {
            $stmt = $con->prepare('UPDATE choices SET text_intrebare=? WHERE id=?');
            $stmt->bindParam(1, $_POST['question'], PDO::PARAM_STR);
            $stmt->bindParam(2, $_POST['idClip'], PDO::PARAM_INT);   
        }
        else {
            $stmt = $con->prepare('INSERT INTO choices (id,text_intrebare) VALUES(?,?)');
            $stmt->bindParam(1, $_POST['idClip'], PDO::PARAM_INT);
            $stmt->bindParam(2, $_POST['question'], PDO::PARAM_STR);
        } 
    }
    $stmt->execute();
}

$target_dir = "/../contents/icons/";
$uploadOk = 1;
if(isset($_FILES["badgeIcon"])) {
$target_file = __DIR__ . $target_dir . basename($_FILES["badgeIcon"]["name"]);
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

// Check if file already exists
/*if (file_exists($target_file)) {
    echo "Sorry, file already exists.";
    //$uploadOk = 0;
}*/
// Check file size
/*if ($_FILES["fileToUpload"]["size"] > 500000) {
    echo "Sorry, your file is too large.";
    $uploadOk = 0;
}*/
// Allow certain file formats
if($imageFileType != "png" && $imageFileType != "jpg" && $imageFileType != "jpeg" && $imageFileType != "gif") {
    echo "Sorry, only [png,jpg,jpeg,gif] files are allowed.";
    $uploadOk = 0;
}
if($uploadOk == 1) {
    move_uploaded_file($_FILES["badgeIcon"]["tmp_name"], $target_file);
}

}

if($_POST['badgeTitle'] != '' && $_POST['badgeDescription'] != '') { //badge valid

    if($badgeId==-1 || $badgeId == null) {  //choice-ul nu are inca badge
        if(isset($_FILES['badgeIcon']) && $uploadOk==1) {
            $stmt = $con->prepare('SELECT MAX(id) as maximum FROM badges');
            $stmt->execute();
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
            if($row['maximum'] == null) $maxIdBadge = 1;
            else $maxIdBadge = $row['maximum'] + 1;

            $stmt = $con->prepare('UPDATE choices SET badge_id=? WHERE id=?');
            $stmt->bindParam(1, $maxIdBadge, PDO::PARAM_INT);
            $stmt->bindParam(2, $_POST['idClip'], PDO::PARAM_INT);
            $stmt->execute();

            $stmt = $con->prepare('INSERT INTO badges VALUES(?,?,?,?,?)');
            $stmt->bindParam(1, $maxIdBadge, PDO::PARAM_INT);
            $stmt->bindParam(2, $_FILES['badgeIcon']['name'], PDO::PARAM_STR);
            $stmt->bindParam(3, $_POST['badgeTitle'], PDO::PARAM_STR);
            $stmt->bindParam(4, $_POST['badgeDescription'], PDO::PARAM_STR);
            $stmt->bindParam(5, $_POST['idClip'], PDO::PARAM_INT);
            $stmt->execute();
        }
        else {
            echo 'You must upload a valid icon for the badge!';
        }
    }
    else {
        if(isset($_FILES['badgeIcon']) && $uploadOk==1) {
            $stmt = $con->prepare('UPDATE badges SET icon_path=?, title=?, description=? WHERE id=?');
            $stmt->bindParam(1, $_FILES['badgeIcon']['name'], PDO::PARAM_STR);
            $stmt->bindParam(2, $_POST['badgeTitle'], PDO::PARAM_STR);
            $stmt->bindParam(3, $_POST['badgeDescription'], PDO::PARAM_STR);
            $stmt->bindParam(4, $badgeId, PDO::PARAM_INT);
        }
        else {
            $stmt = $con->prepare('UPDATE badges SET title=?, description=? WHERE id=?');
            $stmt->bindParam(1, $_POST['badgeTitle'], PDO::PARAM_STR);
            $stmt->bindParam(2, $_POST['badgeDescription'], PDO::PARAM_STR);
            $stmt->bindParam(3, $badgeId, PDO::PARAM_INT);
        }
        $stmt->execute();
    }
}

