document.addEventListener('DOMContentLoaded', () => {
  const uploadBtn = document.getElementById('uploadBtn');
  const imageInput = document.getElementById('imageInput');
  const loading = document.getElementById('loading');

  uploadBtn.addEventListener('click', async () => {
    const file = imageInput.files[0];
    if (!file) {
      alert("Please select an image first.");
      return;
    }

    loading.style.display = 'block';

    const formData = new FormData();
    formData.append('stakeholder', 'farmer');
    formData.append('image', file);

    try {
      const response = await fetch('/submit/farmer', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Upload failed');
      }

      const data = await response.json();
      const batchId = data.batch_id;

      // Redirect to collector.html with parent_batch_id in URL
      window.location.href = `collector.html?parent_batch_id=${batchId}`;
    } catch (err) {
      console.error(err);
      alert("Error uploading image: " + err.message);
    } finally {
      loading.style.display = 'none';
    }
  });
});
