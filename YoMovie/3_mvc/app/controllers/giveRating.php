<?php
require_once '../core/DB.php';
require_once '../core/Model.php';
require_once '../models/Movie.php';
Movie::giveRating($_POST['id'], $_POST['value']);
?>
