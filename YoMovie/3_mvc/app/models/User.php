<?php

class User {
    public $id = 0;
    public $email = '';
    public $username = '';
    public $password = '';
    public $session_id = null;

    function __construct( $email, $username, $password, $session_id) {
        $this->email = $email;
        $this->username = $username;
        $this->password = $password;
        $this->session_id = $session_id;
    }

    public static function checkRegister($model) {
        ;
    }
}