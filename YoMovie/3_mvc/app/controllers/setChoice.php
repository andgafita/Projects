<?php
require_once '../core/DB.php';

$idParinte = $_POST['idParinte'];
$nrChoice = $_POST['nrChoice'];
$choiceText = $_POST['choiceText'];

$con = DB::getInstance()->getConnection();

$stmt = $con->prepare('SELECT movie_id from choices WHERE id=?');
$stmt->bindParam(1, $idParinte, PDO::PARAM_INT);
$stmt->execute();
$row = $stmt->fetch(PDO::FETCH_ASSOC);
$movieId = $row['movie_id'];

$stmt = $con->prepare('SELECT * from choices WHERE id_precedent=? and choice_number=?');
$stmt->bindParam(1, $idParinte, PDO::PARAM_INT);
$stmt->bindParam(2, $nrChoice, PDO::PARAM_INT);
$stmt->execute();
$row = $stmt->fetch(PDO::FETCH_ASSOC);
if($row) {
    $stmt = $con->prepare('UPDATE choices SET descriere=? WHERE id_precedent=? and choice_number=?');
    $stmt->bindParam(1, $choiceText, PDO::PARAM_STR);
    $stmt->bindParam(2, $idParinte, PDO::PARAM_INT);
    $stmt->bindParam(3, $nrChoice, PDO::PARAM_INT);
    $stmt->execute();
}
else {
    $stmt = $con->prepare('SELECT MAX(id) as maximum FROM choices');
    $stmt->execute();
    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    $idMax = $row['maximum'] + 1;
    $stmt = $con->prepare('INSERT INTO choices (id,id_precedent,descriere,choice_number,movie_id,vizualizari) VALUES(?,?,?,?,?,0)');
    $stmt->bindParam(1, $idMax, PDO::PARAM_INT);
    $stmt->bindParam(2, $idParinte, PDO::PARAM_INT);
    $stmt->bindParam(3, $choiceText, PDO::PARAM_STR);
    $stmt->bindParam(4, $nrChoice, PDO::PARAM_INT);
    $stmt->bindParam(5, $movieId, PDO::PARAM_INT);
    $stmt->execute();
    echo $idMax;
}
