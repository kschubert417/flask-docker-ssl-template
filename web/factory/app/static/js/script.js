// Remove page loader
window.addEventListener('load', function () {
    document.querySelector('.page-loading').classList.remove('active');
    setTimeout(function () {
        document.querySelector('.page-loading').remove();
    }, 1000);
});
