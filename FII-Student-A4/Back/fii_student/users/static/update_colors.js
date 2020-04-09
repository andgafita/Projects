
const updateColor = (property, color) => {
    if (color && property) {
        document.documentElement.style.setProperty(property, color);
    }
};

const props = {};

window.onload = () => {
    props.navbar= getComputedStyle(document.documentElement)
        .getPropertyValue('--navbar').trim();
    props.background_first = getComputedStyle(document.documentElement)
        .getPropertyValue('--background-first').trim();
    props.color1_first = getComputedStyle(document.documentElement)
        .getPropertyValue('--color2-first').trim();
    props.color2_first = getComputedStyle(document.documentElement)
        .getPropertyValue('--color2-second').trim();
    props.color1_second = getComputedStyle(document.documentElement)
        .getPropertyValue('--color1-second').trim();
    props.color2_second = getComputedStyle(document.documentElement)
        .getPropertyValue('--color2-second').trim();
    props.font = getComputedStyle(document.documentElement)
        .getPropertyValue('--font').trim();
    props.font_family = getComputedStyle(document.documentElement)
        .getPropertyValue('--font-family').trim();
    console.log(props);
}

function resetProps() {
    // document.documentElement.style
    //     .setProperty('--navbar-color', props.navbar);
}
