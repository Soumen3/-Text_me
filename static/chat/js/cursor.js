document.addEventListener('mousemove', function(e) {
    const cursor = document.querySelector('.cursor');
    cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
});

document.addEventListener('mouseleave', function() {
    const cursor = document.querySelector('.cursor');
    cursor.style.display = 'none';
});

document.addEventListener('mouseenter', function() {
    const cursor = document.querySelector('.cursor');
    cursor.style.display = 'block';
});