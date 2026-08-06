 // Hero carousel -- reads datasets from datasets.js
 (function() {
   const container = document.querySelector(".hero-carousel");
   if (!container || typeof datasets === "undefined" || !datasets.length) return;
 
   const track = container.querySelector(".carousel-track");
   const prevBtn = container.querySelector(".carousel-btn.prev");
   const nextBtn = container.querySelector(".carousel-btn.next");
 
   let index = 0;
   let timer;
 
   function renderSlides() {
     track.innerHTML = datasets.map(function(d) {
       return '<div class="carousel-slide">' +
         '<img src="' + d.imageUrl + '" alt="' + d.title + '" />' +
         '<a class="carousel-caption" href="' + d.detailUrl + '">' + d.title + '</a>' +
         '</div>';
     }).join("");
   }
 
   function goTo(i) {
     index = (i + datasets.length) % datasets.length;
     track.style.transform = "translateX(-" + (index * 100) + "%)";
   }
 
   function next() { goTo(index + 1); }
   function prev() { goTo(index - 1); }
   function startTimer() { timer = setInterval(next, 4000); }
   function resetTimer() { clearInterval(timer); startTimer(); }
 
   renderSlides();
   goTo(0);
   startTimer();
 
   if (prevBtn) prevBtn.addEventListener("click", function() { prev(); resetTimer(); });
   if (nextBtn) nextBtn.addEventListener("click", function() { next(); resetTimer(); });
 })();
