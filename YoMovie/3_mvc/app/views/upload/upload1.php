<?php

class UploadView {
   
    public function content() {
        echo'<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>Upload</title>
            <style>';
        include __DIR__ . '/../../../public/css/style.css';

        echo
        '   </style>
        </head>
        
        <body>
            <div id="wrapper">
        
                <nav>
                        <button onclick="location.href=\'index.html\';">Home</button>
                        <button onclick="location.href=\'index.html\';">Classic movies</button>
                        <button onclick="location.href=\'accountsettings.html\';">Profile</button>
                        <button id="currentButton">Upload</button>
                        <button onclick="location.href=\'LoginSignUp.html\';">Login/Sign up</button>
                </nav>
        
                <div id="videoPageMainContent">
                    <button>Go to previous decision</button>
                    <form action="upload.php" method="post" enctype="multipart/form-data">
                        Select image to upload:
                        <input type="file" name="fileToUpload" id="fileToUpload">
                        <input type="submit" value="Upload Image" name="submit">
                    </form>
                    <button>Upload clip</button>
                    <section id="videoChoiceButtons">
                        <button >Choice: 1</button>
                        <button >Choice: 2</button>
                        <button >+</button>
                    </section>
                </div>
        
        
            </div>
        </body>
        
        </html>';

    }
}