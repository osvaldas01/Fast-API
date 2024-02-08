var slides = document.getElementsByClassName("slide");
        var currentSlide = 0;
        var slideInterval;
        var playButton = document.getElementById("playButton");

        function showSlide(n) {
            for (var i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }
            slides[n].style.display = "block";
        }

        function nextSlide() {
            currentSlide++;
            if (currentSlide >= slides.length) {
                currentSlide = 0;
            }
            showSlide(currentSlide);
        }

        function prevSlide() {
            currentSlide--;
            if (currentSlide < 0) {
                currentSlide = slides.length - 1;
            }
            showSlide(currentSlide);
        }

        function playSlideshow() {
            slideInterval = setInterval(nextSlide, 2000); // Change slide every 2 seconds (adjust as needed)
            playButton.disabled = true; // Disable the "Play" button
        }

        function pauseSlideshow() {
            clearInterval(slideInterval);
        }

        showSlide(currentSlide); // Show the first slide initially