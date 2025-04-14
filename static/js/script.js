document.addEventListener('DOMContentLoaded', function() {
    // Color selection with animation
    const colorButtons = document.querySelectorAll('.color-btn');
    colorButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Animate color change
            this.classList.add('animate__animated', 'animate__pulse');
            setTimeout(() => {
                this.classList.remove('animate__animated', 'animate__pulse');
            }, 300);
            
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
    
    // Brush size control with animation
    const brushSlider = document.getElementById('brush-slider');
    const brushSizeDisplay = document.getElementById('brush-size');
    
    brushSlider.addEventListener('input', function() {
        const size = this.value;
        brushSizeDisplay.textContent = size;
        
        // Add animation to brush size display
        brushSizeDisplay.classList.add('animate__animated', 'animate__bounceIn');
        setTimeout(() => {
            brushSizeDisplay.classList.remove('animate__animated', 'animate__bounceIn');
        }, 300);
        
        fetch('/change_brush', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `size=${size}`
        });
    });
    
    // Clear canvas button with animation
    const clearBtn = document.getElementById('clear-btn');
    clearBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Add click animation
        this.classList.add('animate__animated', 'animate__rubberBand');
        setTimeout(() => {
            this.classList.remove('animate__animated', 'animate__rubberBand');
        }, 300);
        
        fetch('/clear', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        }).then(() => {
            // Show confirmation animation
            const videoContainer = document.querySelector('.video-container');
            videoContainer.classList.add('animate__animated', 'animate__fadeOut');
            setTimeout(() => {
                videoContainer.classList.remove('animate__animated', 'animate__fadeOut');
                videoContainer.classList.add('animate__animated', 'animate__fadeIn');
                setTimeout(() => {
                    videoContainer.classList.remove('animate__animated', 'animate__fadeIn');
                }, 300);
            }, 300);
        });
    });
    
    // Save button animation
    const saveBtn = document.getElementById('save-btn');
    saveBtn.addEventListener('click', function() {
        this.classList.add('animate__animated', 'animate__tada');
        setTimeout(() => {
            this.classList.remove('animate__animated', 'animate__tada');
        }, 300);
    });
    
    // Toggle instructions
    const instructionsHeader = document.querySelector('.instructions-header');
    const instructionsContent = document.querySelector('.instructions-content');
    const toggleInstructions = document.querySelector('.toggle-instructions');
    
    instructionsHeader.addEventListener('click', function() {
        if (instructionsContent.style.maxHeight) {
            instructionsContent.style.maxHeight = null;
            toggleInstructions.textContent = '+';
        } else {
            instructionsContent.style.maxHeight = instructionsContent.scrollHeight + 'px';
            toggleInstructions.textContent = '−';
        }
    });
    
    // Initialize instructions as expanded
    instructionsContent.style.maxHeight = instructionsContent.scrollHeight + 'px';
});toggleInstructions.textContent = '−'; // Ensure minus sign is shown initially
