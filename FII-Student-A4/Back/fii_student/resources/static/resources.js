const filters = ['internal', 'external'];
var active = document.getElementsByClassName("show-all")[0];

function setActive(btn) {
    btn.style.background = "linear-gradient(to right, var(--color1-first) 0%, var(--color1-second) 100%)";
    btn.style.outline = "none";
    btn.style.outline = "none";
}

function unsetActive(btn) {
    btn.style.background = "var(--background-second)";
    btn.style.outline = "none";
}


filters.forEach(element => {
    const btn = document.getElementsByClassName(element)[0];
    btn.addEventListener("click", () => {
        unsetActive(active);
        active = btn;
        setActive(active);

        const listItems = document.getElementsByClassName('resources-item');
        let parity = 0;
        for (let i = 0; i < listItems.length; i++) {
            const itemFilterType = listItems[i].getAttribute('data-type');

            if (itemFilterType === element) {
                listItems[i].style.display = "";
                if (parity % 2 == 0) {
                    listItems[i].classList.remove("odd");
                    listItems[i].classList.add("even");
                }
                else {
                    listItems[i].classList.remove("even");
                    listItems[i].classList.add("odd");
                }
                parity++;
            } else {
                listItems[i].style.display = "none";
            }
        }

    });
});

const btnShowAll = document.getElementsByClassName("show-all")[0];
setActive(btnShowAll);
btnShowAll.addEventListener("click", () => {
    unsetActive(active);
    active = btnShowAll;
    setActive(active);
    const listItems = document.getElementsByClassName('resources-item');
    let parity = 0;
    for (let i = 0; i < listItems.length; i++) {
        listItems[i].style.display = "";
        if (parity % 2 == 0) {
            listItems[i].classList.remove("odd");
            listItems[i].classList.add("even");
        }
        else {
            listItems[i].classList.remove("even");
            listItems[i].classList.add("odd");
        }
        parity++;
    }
});

window.onload = function () {
    const listItems = document.getElementsByClassName('resources-item');
    let parity = 0;
    for (let i = 0; i < listItems.length; i++) {
        listItems[i].style.display = "";
        if (parity % 2 == 0) {
            listItems[i].classList.remove("odd");
            listItems[i].classList.add("even");
        }
        else {
            listItems[i].classList.remove("even");
            listItems[i].classList.add("odd");
        }
        parity++;
    }
}
