document.addEventListener('DOMContentLoaded', () => {
  const parentBatchInput = document.getElementById('parent_batch_id');
  const weightInput = document.getElementById('weight');
  const reportInput = document.getElementById('report');
  const generateBtn = document.getElementById('generateBtn');
  const form = document.getElementById('processor2Form');

  // Enable submit button only if weight + report filled
  const checkFormValidity = () => {
    generateBtn.disabled = !(weightInput.value && reportInput.files.length > 0);
  };

  weightInput.addEventListener('input', checkFormValidity);
  reportInput.addEventListener('change', checkFormValidity);

  // Pre-fill parent_batch_id from URL
  const urlParams = new URLSearchParams(window.location.search);
  const parentBatchId = urlParams.get('parent_batch_id');
  if (parentBatchId) {
    parentBatchInput.value = parentBatchId;
    checkFormValidity();
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = new FormData();
    payload.append('parent_batch_id', parentBatchInput.value);
    payload.append('weight', weightInput.value);
    payload.append('stakeholder', 'processing2');
    payload.append('report', reportInput.files[0]);

    try {
      const response = await fetch('http://localhost:8000/submit/processing2', {
        method: 'POST',
        body: payload
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Submission failed');
      }

      const data = await response.json();

      // Redirect to processor2batchID.html with new batch ID
      window.location.href = `processor2batchID.html?parent_batch_id=${parentBatchInput.value}&new_batch_id=${data.batch_id}`;

    } catch (err) {
      console.error(err);
      alert("Error submitting form: " + err.message);
    }
  });
});
