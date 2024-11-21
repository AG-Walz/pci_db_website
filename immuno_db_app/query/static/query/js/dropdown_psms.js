var dropdownContainers = document.querySelectorAll('.dropdown-check-list');

dropdownContainers.forEach(function (container) {
    var items = container.querySelector('.items');
    var anchor = container.querySelector('.anchor');

    anchor.onclick = function (evt) {
        if (items.classList.contains('visible')) {
            items.classList.remove('visible');
            items.style.display = "none";
        } else {
            items.classList.add('visible');
            items.style.display = "block";
        }
        evt.stopPropagation(); // Prevent the click event from bubbling up
    };

    // Attach a click event listener to the document to close the dropdown
    document.addEventListener('click', function (event) {
        if (!container.contains(event.target)) {
            items.classList.remove('visible');
            items.style.display = "none";
        }
    });

    // Handle blur event on the items element
    items.onblur = function (evt) {
        items.classList.remove('visible');
        items.style.display = "none";
    };
});