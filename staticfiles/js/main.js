// Main Minimalist Interactive JavaScript for Coffee Shop
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. AJAX Add to Cart Handler
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const productId = btn.dataset.productId;
            const grindType = btn.dataset.grind || 'دانه کامل';
            
            const formData = new FormData();
            formData.append('product_id', productId);
            formData.append('quantity', 1);
            formData.append('grind_type', grindType);
            
            fetch('/cart/api/add/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const badges = document.querySelectorAll('.cart-badge');
                    badges.forEach(badge => badge.textContent = data.cart_total_items);
                    showNotification(data.message || 'به سبد خرید اضافه شد!', 'success');
                }
            })
            .catch(err => console.error('Cart Error:', err));
        });
    });

    // 2. Soundscape Audio Generator
    let audioCtx = null;
    let isSoundPlaying = false;
    const soundToggle = document.getElementById('soundscapeToggle');

    if (soundToggle) {
        soundToggle.addEventListener('click', () => {
            if (!isSoundPlaying) {
                startCafeAmbience();
                soundToggle.classList.add('playing');
                soundToggle.querySelector('span').textContent = 'صدای کافه (روشن 🎵)';
            } else {
                stopCafeAmbience();
                soundToggle.classList.remove('playing');
                soundToggle.querySelector('span').textContent = 'صدای کافه';
            }
        });
    }

    function startCafeAmbience() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        isSoundPlaying = true;
    }

    function stopCafeAmbience() {
        if (audioCtx) {
            audioCtx.suspend();
        }
        isSoundPlaying = false;
    }

    // Helper: Toast Notification
    function showNotification(msg, type = 'info') {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed; bottom: 2rem; left: 2rem; z-index: 9999;
            background: #15181E; border: 1px solid #FF7A00; color: #FFF;
            padding: 10px 20px; border-radius: 50px; font-weight: 600; font-size: 0.9rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.6); animation: fadeInUp 0.3s ease;
        `;
        toast.innerHTML = `<i class="fa-solid fa-circle-check" style="color:#FF7A00; margin-left:8px;"></i> ${msg}`;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    // Helper: Get Django CSRF Cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
