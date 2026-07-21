(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function showToast(message) {
    var toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.remove('opacity-0', 'translate-y-4');
    toast.classList.add('opacity-100', 'translate-y-0');
    window.clearTimeout(showToast._timer);
    showToast._timer = window.setTimeout(function () {
      toast.classList.add('opacity-0', 'translate-y-4');
      toast.classList.remove('opacity-100', 'translate-y-0');
    }, 2200);
  }

  // Back-to-top button
  var backToTop = document.getElementById('back-to-top');
  if (backToTop) {
    var toggleBackToTop = function () {
      var shouldShow = window.scrollY > 480;
      backToTop.classList.toggle('hidden', !shouldShow);
      backToTop.classList.toggle('flex', shouldShow);
    };
    window.addEventListener('scroll', toggleBackToTop, { passive: true });
    toggleBackToTop();

    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
    });
  }

  // Copy product link (product detail page)
  var copyLinkBtn = document.querySelector('[data-copy-link]');
  if (copyLinkBtn) {
    copyLinkBtn.addEventListener('click', function () {
      var url = window.location.href;
      var done = function () { showToast('คัดลอกลิงก์แล้ว'); };
      var fail = function () { showToast('ไม่สามารถคัดลอกลิงก์ได้'); };

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, fail);
      } else {
        var input = document.createElement('input');
        input.value = url;
        document.body.appendChild(input);
        input.select();
        try {
          document.execCommand('copy');
          done();
        } catch (err) {
          fail();
        }
        document.body.removeChild(input);
      }
    });
  }

  // Quantity stepper (product detail page, UI only)
  var qtyValue = document.querySelector('[data-qty-value]');
  if (qtyValue) {
    var qtyDecrease = document.querySelector('[data-qty-decrease]');
    var qtyIncrease = document.querySelector('[data-qty-increase]');
    var qty = parseInt(qtyValue.textContent, 10) || 1;
    var MIN_QTY = 1;
    var MAX_QTY = 99;

    var render = function () { qtyValue.textContent = String(qty); };

    if (qtyDecrease) {
      qtyDecrease.addEventListener('click', function () {
        qty = Math.max(MIN_QTY, qty - 1);
        render();
      });
    }
    if (qtyIncrease) {
      qtyIncrease.addEventListener('click', function () {
        qty = Math.min(MAX_QTY, qty + 1);
        render();
      });
    }
  }

  // Debounced auto-submit for the search input (product list page)
  var filterForm = document.getElementById('filter-form');
  if (filterForm) {
    var searchInput = filterForm.querySelector('input[name="q"]');
    if (searchInput) {
      var debounceTimer;
      searchInput.addEventListener('input', function () {
        window.clearTimeout(debounceTimer);
        debounceTimer = window.setTimeout(function () {
          filterForm.submit();
        }, 500);
      });
    }
  }
})();
