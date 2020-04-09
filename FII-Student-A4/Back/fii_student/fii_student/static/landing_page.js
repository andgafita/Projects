var bodyContainer = document.getElementById("bodyContainer");
var learnMoreBtn = document.getElementById("learnMoreButton");
var learnMorePopUp = document.getElementById("learnMorePopUp");
var popUpCloseBtn = document.getElementById("closePopUpButton");


learnMoreBtn.addEventListener('click', event => {
    learnMorePopUp.style.display = "block";
});

popUpCloseBtn.addEventListener('click', event => {
    learnMorePopUp.style.display = "none";
});

bodyContainer.addEventListener('click', event => {
    if (event.target != learnMoreBtn && event.target != learnMorePopUp && event.target.parentNode != learnMorePopUp) {
        learnMorePopUp.style.display = "none";
    }
});