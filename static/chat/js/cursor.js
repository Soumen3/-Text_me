document.addEventListener('mousemove', function(e) {
    const cursor = document.querySelector('.cursor');  
    cursor.style.transform = `translate(${e.pageX}px, ${e.pageY}px)`;
});

document.addEventListener('mouseleave', function() {
    const cursor = document.querySelector('.cursor');
    cursor.style.display = 'none';
});

document.addEventListener('mouseenter', function() {
    const cursor = document.querySelector('.cursor');
    cursor.style.display = 'block';
});