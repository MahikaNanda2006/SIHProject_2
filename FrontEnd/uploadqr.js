document.addEventListener('DOMContentLoaded', () => {
  const qrUpload = document.getElementById('qrUpload');
  const findHistoryBtn = document.getElementById('findHistoryBtn');

  let batchId = null;

  qrUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, canvas.width, canvas.height);

        if (code) {
          batchId = code.data;
          sessionStorage.setItem('uploadedBatchId', batchId); // store for next page
          findHistoryBtn.disabled = false;
        } else {
          alert("No QR code found. Please try again.");
          findHistoryBtn.disabled = true;
        }
      };
      img.src = event.target.result;
    };
    reader.readAsDataURL(file);
  });

  findHistoryBtn.addEventListener('click', () => {
  if (!batchId) {
    alert("Batch ID not found!");
    return;
  }
  // Pass batch_id as URL parameter
  window.location.href = `customer-interface.html?batch_id=${batchId}`;
});

});
