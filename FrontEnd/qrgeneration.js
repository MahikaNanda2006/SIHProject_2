document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const batchId = urlParams.get('batch_id');

  if (!batchId) {
    alert("No batch ID found!");
    return;
  }

  document.getElementById('batchIdDisplay').textContent = batchId;

  const qrCanvas = document.getElementById('qrCode');
  QRCode.toCanvas(qrCanvas, batchId, { width: 200 }, (error) => {
    if (error) console.error(error);
  });

  // Store batch ID in sessionStorage for the next page
  sessionStorage.setItem('generatedBatchId', batchId);

  // Download functionality
  const downloadBtn = document.getElementById('downloadBtn');
  downloadBtn.addEventListener('click', () => {
    const link = document.createElement('a');
    link.download = `Batch_${batchId}_QR.png`;
    link.href = qrCanvas.toDataURL('image/png'); // convert canvas to PNG
    link.click();
  });

  // Next button to go to uploadqr.html
  const nextBtn = document.getElementById('nextBtn');
  nextBtn.addEventListener('click', () => {
    window.location.href = 'uploadqr.html';
  });
});
