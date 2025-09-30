document.addEventListener('DOMContentLoaded', () => {
  const batchInput = document.getElementById('batchId');
  const speciesInput = document.getElementById('speciesName');
  const weightInput = document.getElementById('weight');
  const verificationInput = document.getElementById('verification');
  const generateBtn = document.getElementById('generateBtn');

  const form = document.getElementById('collectorForm');

  // Modal elements
  const modal = document.getElementById('confirmationModal');
  const generatedIdEl = document.getElementById('generatedId');
  const confirmBatchId = document.getElementById('confirmBatchId');
  const confirmSpecies = document.getElementById('confirmSpecies');
  const confirmWeight = document.getElementById('confirmWeight');
  const closeModal = document.getElementById('closeModal');
  const nextBtn = document.getElementById('newCollection'); // repurposed as Next

  // Enable button only if all fields filled + verified
  const checkFormValidity = () => {
    generateBtn.disabled = !(batchInput.value && speciesInput.value && weightInput.value && verificationInput.checked);
  };
  batchInput.addEventListener('input', checkFormValidity);
  speciesInput.addEventListener('input', checkFormValidity);
  weightInput.addEventListener('input', checkFormValidity);
  verificationInput.addEventListener('change', checkFormValidity);

  // Pre-fill parent_batch_id from URL
  const urlParams = new URLSearchParams(window.location.search);
  const parentBatchId = urlParams.get('parent_batch_id');
  if (parentBatchId) {
    batchInput.value = parentBatchId;
    checkFormValidity();
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = new FormData();
    payload.append('parent_batch_id', batchInput.value);
    payload.append('crop_name', speciesInput.value);
    payload.append('weight', weightInput.value);
    payload.append('stakeholder', 'collector');

    try {
      const response = await fetch('http://localhost:8000/submit/collector', {
        method: 'POST',
        body: payload
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Submission failed');
      }

      const data = await response.json();
      // Show modal with returned batch_id
      const collectorBatchId = data.batch_id;
      generatedIdEl.textContent = collectorBatchId;
      confirmBatchId.textContent = batchInput.value;
      confirmSpecies.textContent = speciesInput.value;
      confirmWeight.textContent = weightInput.value;

      modal.style.display = 'flex';

      // Store collector batch id in the Next button dataset
      nextBtn.dataset.collectorBatchId = collectorBatchId;

    } catch (err) {
      console.error(err);
      alert("Error submitting form: " + err.message);
    }
  });

  closeModal.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  // Next button redirects to processor1.html with parent_batch_id
  nextBtn.addEventListener('click', () => {
  const collectorBatchId = generatedIdEl.textContent; // use the actual displayed ID
  if (collectorBatchId) {
    // Redirect to processor1.html with query param
    window.location.href = `processor1.html?parent_batch_id=${collectorBatchId}`;
  }
});

});
