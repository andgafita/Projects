<?php
require_once '../core/DB.php';
$idClip = $_POST['idChoice'];

$con = DB::getInstance()->getConnection();
$stmt = $con->prepare('SELECT id FROM choices WHERE vizualizari=(SELECT MAX(vizualizari) FROM
choices WHERE id_precedent=?) AND id_precedent=?');

$stmt->bindParam(1, $idClip, PDO::PARAM_INT);
$stmt->bindParam(2, $idClip, PDO::PARAM_INT);
$stmt->execute();
$row = $stmt->fetch(PDO::FETCH_ASSOC);
echo $row['id'];
