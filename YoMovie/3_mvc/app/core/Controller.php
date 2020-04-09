<?php

class Controller {
    public function model($model) {
        require_once '../app/models/' . $model . '.php';
    }

    public function view($view, $data = [], $model = null) {
        require_once '../app/views/' . $view . '.php';
    }
}