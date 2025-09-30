document.addEventListener('DOMContentLoaded', () => {
  const parentBatchInput = document.getElementById('parent_batch_id');
  const reportInput = document.getElementById('report');
  const generateBtn = document.getElementById('generateBtn');
  const form = document.getElementById('packagingForm');

  // Enable button only if PDF selected
  reportInput.addEventListener('change', () => {
    generateBtn.disabled = !(reportInput.files.length > 0);
  });

  // Pre-fill parent_batch_id from URL
  const urlParams = new URLSearchParams(window.location.search);
  const parentBatchId = urlParams.get('parent_batch_id');
  if (parentBatchId) parentBatchInput.value = parentBatchId;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = new FormData();
    payload.append('parent_batch_id', parentBatchInput.value);
    payload.append('stakeholder', 'packaging');
    payload.append('report', reportInput.files[0]);

    try {
      const response = await fetch('http://localhost:8000/submit/packaging', {
        method: 'POST',
        body: payload
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Submission failed');
      }

      const data = await response.json();
      const newBatchId = data.batch_id;

      // Redirect to QR generation page
      window.location.href = `qrgeneration.html?batch_id=${newBatchId}`;

    } catch (err) {
      console.error(err);
      alert("Error submitting form: " + err.message);
    }
  });
});
