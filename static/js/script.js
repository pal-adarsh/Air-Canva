document.addEventListener('DOMContentLoaded', function() {
    // Color selection
    const colorButtons = document.querySelectorAll('.color-btn');
    colorButtons.forEach(button => {
        button.addEventListener('click', function() {
            colorButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const color = this.dataset.color;
            
            fetch('/change_color', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `color=${color}`
            });
        });
    });
    
    // Brush size control
    const brushSlider = document.getElementById('brush-slider');
    const brushSizeDisplay = document.getElementById('brush-size');
    
    brushSlider.addEventListener('input', function() {
        const size = this.value;
        brushSizeDisplay.textContent = size;
        
        fetch('/change_brush', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `size=${size}`
        });
    });
    
    // Clear canvas button
    document.getElementById('clear-btn').addEventListener('click', function() {
        fetch('/clear', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
    });
});