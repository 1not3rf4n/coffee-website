document.addEventListener('DOMContentLoaded', () => {
    const navToggleBtn = document.getElementById('navToggleBtn');
    const mobileDrawer = document.getElementById('mobileDrawer');
    const drawerOverlay = document.getElementById('drawerOverlay');
    const drawerCloseBtn = document.getElementById('drawerCloseBtn');

    function openDrawer() {
        if (mobileDrawer) mobileDrawer.classList.add('active');
        if (drawerOverlay) drawerOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        if (mobileDrawer) mobileDrawer.classList.remove('active');
        if (drawerOverlay) drawerOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (navToggleBtn) navToggleBtn.addEventListener('click', openDrawer);
    if (drawerCloseBtn) drawerCloseBtn.addEventListener('click', closeDrawer);
    if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeDrawer();
    });

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
                    updateCartBadges(data.cart_total_items);
                    showToast(data.message || 'به سبد خرید اضافه شد!', 'success');
                }
            })
            .catch(err => console.error(err));
        });
    });

    function updateCartBadges(count) {
        const badges = document.querySelectorAll('.cart-badge');
        badges.forEach(b => {
            b.textContent = count;
            b.style.display = count > 0 ? 'flex' : 'none';
        });
    }

    const cartContainer = document.getElementById('cartContainer');
    if (cartContainer) {
        cartContainer.addEventListener('click', (e) => {
            const incBtn = e.target.closest('.cart-qty-inc');
            const decBtn = e.target.closest('.cart-qty-dec');
            const delBtn = e.target.closest('.cart-item-del');

            if (incBtn || decBtn) {
                const row = (incBtn || decBtn).closest('.cart-row');
                const key = row.dataset.key;
                const qtyEl = row.querySelector('.qty-val');
                let currentQty = parseInt(qtyEl.textContent) || 1;
                let newQty = incBtn ? currentQty + 1 : currentQty - 1;

                if (newQty <= 0) {
                    removeCartItem(key, row);
                    return;
                }

                const formData = new FormData();
                formData.append('item_key', key);
                formData.append('quantity', newQty);

                fetch('/cart/api/update/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCookie('csrftoken') },
                    body: formData
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        qtyEl.textContent = newQty;
                        updateCartBadges(data.cart_total_items);
                        const unitPrice = parseInt(row.dataset.price);
                        const lineTotalEl = row.querySelector('.cart-line-total');
                        if (lineTotalEl) lineTotalEl.textContent = (unitPrice * newQty).toLocaleString('fa-IR') + ' تومان';
                        updateTotalPrice(data.cart_total_price);
                    }
                });
            }

            if (delBtn) {
                const row = delBtn.closest('.cart-row');
                const key = row.dataset.key;
                removeCartItem(key, row);
            }
        });
    }

    function removeCartItem(key, row) {
        const formData = new FormData();
        formData.append('item_key', key);
        fetch('/cart/api/remove/', {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                row.remove();
                updateCartBadges(data.cart_total_items);
                updateTotalPrice(data.cart_total_price);
                if (data.cart_total_items === 0) {
                    location.reload();
                }
            }
        });
    }

    function updateTotalPrice(total) {
        const totalEl = document.getElementById('cartTotalPrice');
        if (totalEl) {
            totalEl.textContent = total.toLocaleString('fa-IR') + ' تومان';
        }
    }

    // ──────────────────────────────────────────────────────────────────────────
    // سیستم پیشرفته موزیک کافه (پلی‌لیست، پخش تصادفی Shuffle و پخش خودکار Autoplay)
    // ──────────────────────────────────────────────────────────────────────────
    const musicPlayerElem = document.getElementById('cafeMusicPlayer');
    const audioElement = document.getElementById('cafeAudioElement');
    const musicToggleBtn = document.getElementById('musicToggleBtn');
    const musicPlayIcon = document.getElementById('musicPlayIcon');
    const musicNextBtn = document.getElementById('musicNextBtn');
    const musicTitleDisplay = document.getElementById('musicTitleDisplay');
    const musicArtistDisplay = document.getElementById('musicArtistDisplay');
    const playlistDataScript = document.getElementById('cafePlaylistData');

    if (musicPlayerElem && audioElement && playlistDataScript) {
        let playlist = [];
        try {
            playlist = JSON.parse(playlistDataScript.textContent || '[]');
        } catch (e) {
            playlist = [];
        }

        if (playlist.length === 0) {
            playlist = [{
                title: 'صدای ملایم کافه',
                artist: 'نوین کافه',
                url: 'https://assets.mixkit.co/music/preview/mixkit-chill-bro-494.mp3'
            }];
        }

        let currentIndex = Math.floor(Math.random() * playlist.length);
        let isPlaying = false;
        let userHasPaused = sessionStorage.getItem('cafe_music_user_paused') === 'true';
        const shouldAutoplay = musicPlayerElem.dataset.autoplay === 'true';

        audioElement.volume = 0.40;

        function loadTrack(index) {
            if (index < 0 || index >= playlist.length) index = 0;
            currentIndex = index;
            const track = playlist[currentIndex];
            audioElement.src = track.url;
            if (musicTitleDisplay) musicTitleDisplay.textContent = track.title;
            if (musicArtistDisplay) musicArtistDisplay.textContent = track.artist || 'کافه عرفان';
        }

        function playMusic() {
            if (!audioElement.src) {
                loadTrack(currentIndex);
            }
            audioElement.play().then(() => {
                isPlaying = true;
                userHasPaused = false;
                sessionStorage.removeItem('cafe_music_user_paused');
                musicPlayerElem.classList.add('playing');
                if (musicPlayIcon) {
                    musicPlayIcon.classList.remove('fa-play');
                    musicPlayIcon.classList.add('fa-pause');
                }
            }).catch(err => {
                console.log('Autoplay deferred until user interaction:', err);
                setupInteractionAutoplay();
            });
        }

        function pauseMusic() {
            audioElement.pause();
            isPlaying = false;
            userHasPaused = true;
            sessionStorage.setItem('cafe_music_user_paused', 'true');
            musicPlayerElem.classList.remove('playing');
            if (musicPlayIcon) {
                musicPlayIcon.classList.remove('fa-pause');
                musicPlayIcon.classList.add('fa-play');
            }
        }

        function playNextShuffle() {
            if (playlist.length > 1) {
                let nextIndex;
                do {
                    nextIndex = Math.floor(Math.random() * playlist.length);
                } while (nextIndex === currentIndex);
                currentIndex = nextIndex;
            } else {
                currentIndex = 0;
            }
            loadTrack(currentIndex);
            playMusic();
        }

        // هندلر پخش خودکار هوشمند با اولین لمس یا اسکرول اگر مرورگر در ابتدا اجازه نداد
        function setupInteractionAutoplay() {
            if (userHasPaused) return;
            const onFirstInteraction = () => {
                if (!isPlaying && !userHasPaused) {
                    playMusic();
                }
                ['click', 'touchstart', 'scroll', 'keydown'].forEach(evt => {
                    window.removeEventListener(evt, onFirstInteraction, { passive: true });
                });
            };
            ['click', 'touchstart', 'scroll', 'keydown'].forEach(evt => {
                window.addEventListener(evt, onFirstInteraction, { once: true, passive: true });
            });
        }

        // رویداد پایان هر آهنگ (پخش خودکار آهنگ بعدی به صورت تصادفی)
        audioElement.addEventListener('ended', () => {
            playNextShuffle();
        });

        // دکمه کنترل قطع و وصل
        if (musicToggleBtn) {
            musicToggleBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (isPlaying) {
                    pauseMusic();
                } else {
                    playMusic();
                }
            });
        }

        // دکمه موزیک بعدی
        if (musicNextBtn) {
            musicNextBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                playNextShuffle();
            });
        }

        // راه‌اندازی اولیه
        loadTrack(currentIndex);
        if (shouldAutoplay && !userHasPaused) {
            playMusic();
        }
    }

    const wheelCanvas = document.getElementById('wheelCanvas');
    const spinBtn = document.getElementById('spinWheelBtn');
    const wheelResult = document.getElementById('wheelResult');

    if (wheelCanvas && spinBtn) {
        const ctx = wheelCanvas.getContext('2d');
        const prizes = [
            '۱۰٪ تخفیف', 'ارسال رایگان', 'قهوه رایگان',
            '۱۵٪ تخفیف', 'کوکی هدیه', '۵٪ تخفیف',
            '۲۰٪ تخفیف', 'شات دبل رایگان'
        ];
        const colors = ['#E65100', '#2E3238', '#F57C00', '#1F2124', '#EF6C00', '#2E3238', '#FF9800', '#1F2124'];
        const numSegments = prizes.length;
        const arc = (2 * Math.PI) / numSegments;
        let currentRotation = 0;
        let isSpinning = false;

        function drawWheel() {
            const centerX = wheelCanvas.width / 2;
            const centerY = wheelCanvas.height / 2;
            const radius = centerX - 8;

            ctx.clearRect(0, 0, wheelCanvas.width, wheelCanvas.height);

            for (let i = 0; i < numSegments; i++) {
                const angle = i * arc;
                ctx.beginPath();
                ctx.fillStyle = colors[i];
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, angle, angle + arc);
                ctx.lineTo(centerX, centerY);
                ctx.fill();
                ctx.strokeStyle = 'rgba(255,255,255,0.15)';
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.save();
                ctx.translate(centerX, centerY);
                ctx.rotate(angle + arc / 2);
                ctx.textAlign = 'right';
                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 13px Vazirmatn, sans-serif';
                ctx.fillText(prizes[i], radius - 20, 5);
                ctx.restore();
            }
        }

        drawWheel();

        spinBtn.addEventListener('click', () => {
            if (isSpinning) return;
            isSpinning = true;
            spinBtn.disabled = true;

            fetch('/api/spin-wheel/')
                .then(res => res.json())
                .then(data => {
                    const extraRounds = 5 + Math.floor(Math.random() * 4);
                    const randomSegment = Math.floor(Math.random() * numSegments);
                    const stopAngle = (extraRounds * 360) + (randomSegment * (360 / numSegments)) + (360 / (numSegments * 2));
                    currentRotation += stopAngle;

                    wheelCanvas.style.transition = 'transform 4.5s cubic-bezier(0.15, 0.9, 0.25, 1)';
                    wheelCanvas.style.transform = `rotate(${currentRotation}deg)`;

                    setTimeout(() => {
                        isSpinning = false;
                        spinBtn.disabled = false;
                        if (wheelResult) {
                            wheelResult.style.display = 'block';
                            document.getElementById('wheelCodeText').textContent = data.code || 'COFFEE10';
                            document.getElementById('wheelPrizeTitle').textContent = data.title || 'تخفیف ویژه کافه';
                        }
                        showToast(`تبریک! کد تخفیف شما: ${data.code}`, 'success');
                    }, 4800);
                })
                .catch(() => {
                    isSpinning = false;
                    spinBtn.disabled = false;
                });
        });
    }

    const copyCodeBtn = document.getElementById('copyWheelCodeBtn');
    if (copyCodeBtn) {
        copyCodeBtn.addEventListener('click', () => {
            const code = document.getElementById('wheelCodeText').textContent;
            navigator.clipboard.writeText(code).then(() => {
                showToast('کد تخفیف در کلیپ‌بورد کپی شد!', 'success');
            });
        });
    }

    function showToast(msg, type = 'info') {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        const toast = document.createElement('div');
        toast.className = 'toast-msg';
        toast.innerHTML = `<i class="fa-solid fa-circle-check" style="color:var(--ember);"></i> <span>${msg}</span>`;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 3500);
    }

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
