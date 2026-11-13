// ========================================================
// Customer Complaint Classification - Frontend Scripts
// ========================================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Sidebar Toggle
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });

    // Close when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
        if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target) && sidebar.classList.contains('open')) {
          sidebar.classList.remove('open');
        }
      }
    });
  }

  // 2. Complaint Classification Form
  const classifyForm = document.getElementById('classifyForm');
  const complaintInput = document.getElementById('complaintInput');
  const modelSelect = document.getElementById('modelSelect');
  const clearBtn = document.getElementById('clearBtn');
  const resultCard = document.getElementById('resultCard');
  const submitBtn = document.getElementById('submitBtn');

  if (classifyForm) {
    // Fill sample complaints
    const samplePills = document.querySelectorAll('.sample-pill');
    samplePills.forEach(pill => {
      pill.addEventListener('click', () => {
        const sampleText = pill.getAttribute('data-sample');
        if (complaintInput) {
          complaintInput.value = sampleText;
          complaintInput.focus();
        }
      });
    });

    // Clear button action
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        if (complaintInput) complaintInput.value = '';
        if (resultCard) resultCard.style.display = 'none';
      });
    }

    // Submit classification
    classifyForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const text = complaintInput ? complaintInput.value.trim() : '';
      const model = modelSelect ? modelSelect.value : 'logistic_regression';

      if (!text) {
        showToast('Please enter a complaint text to classify.', 'error');
        if (complaintInput) complaintInput.focus();
        return;
      }

      // Show loading state
      const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Classify';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
          <svg class="spinner" style="width:16px;height:16px;animation:spin 1s linear infinite;" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" stroke-width="4" stroke-opacity="0.25"></circle>
            <path d="M4 12a8 8 0 018-8" stroke-width="4"></path>
          </svg>
          Processing...
        `;
      }

      try {
        const response = await fetch('/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text, model })
        });

        const data = await response.json();

        if (data.success) {
          displayResult(data);
          showToast(`Successfully classified as ${data.category}`, 'success');
        } else {
          showToast(data.error || 'Prediction failed.', 'error');
        }
      } catch (err) {
        showToast('Error connecting to classification server.', 'error');
        console.error(err);
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnText;
        }
      }
    });
  }
});

// Render classification results
function displayResult(data) {
  const resultCard = document.getElementById('resultCard');
  const resCategory = document.getElementById('resCategory');
  const resModel = document.getElementById('resModel');
  const resCleaned = document.getElementById('resCleaned');

  if (resCategory) resCategory.textContent = data.category;
  if (resModel) resModel.textContent = data.model_name;
  if (resCleaned) resCleaned.textContent = data.cleaned_text || '(none)';

  if (resultCard) {
    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

// Toast notification helper
function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span>${message}</span>
    <button style="background:none;border:none;color:inherit;cursor:pointer;font-size:16px;" onclick="this.parentElement.remove()">×</button>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(30px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

