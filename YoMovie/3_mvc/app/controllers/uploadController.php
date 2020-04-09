<?php

class UploadController extends Controller {
    public function index() {
        echo 'mama';
    }
    public function upload($clipNr = 0) {
        $this->model('Choice');
        $this->model('Badge');
        $choice = new Choice($clipNr);
        $badge = new Badge($choice->badgeId);
        $this->view('upload/upload',['childNodes'=>Choice::getAllChildNodes($clipNr),'badge'=>$badge], $choice);
        //$vi = new UploadView();
        //$vi->content();
    }
}