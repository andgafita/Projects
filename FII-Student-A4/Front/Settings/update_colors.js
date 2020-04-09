
const updateColor = (property, color) => {
    if (color && property) {
        document.documentElement.style.setProperty(property, color);
    }
};

const props = {};

window.onload = () => {
    props.navbar = getComputedStyle(document.documentElement)
        .getPropertyValue('--navbar').trim();
    props.background = getComputedStyle(document.documentElement)
        .getPropertyValue('--background').trim();
    props.accent = getComputedStyle(document.documentElement)
        .getPropertyValue('--accent').trim();
    props.font = getComputedStyle(document.documentElement)
        .getPropertyValue('--font').trim();
    props.family = getComputedStyle(document.documentElement)
        .getPropertyValue('--font-family').trim();
    console.log(props);
}

function resetProps() {
    document.documentElement.style
        .setProperty('--navbar', props.navbar);
}
