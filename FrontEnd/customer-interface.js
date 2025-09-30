document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const batchId = urlParams.get('batch_id');

  if (!batchId) {
    alert("No batch ID found!");
    return;
  }

  const container = document.getElementById('historyContainer');
  container.innerHTML = "Loading...";

  try {
    const response = await fetch(`http://localhost:8000/api/trace/${batchId}`);
    if (!response.ok) throw new Error("Batch not found");
    const data = await response.json();
    const history = data.trace;

    container.innerHTML = ""; // clear loading text

    history.forEach((record, index) => {
      // Create step box
      const stepBox = document.createElement('div');
      stepBox.classList.add('step-box');

      // Build HTML for this box
      let html = `
        <strong>${record.stakeholder.toUpperCase()}</strong>
        <p><strong>Batch ID:</strong> ${record.batch_id}</p>
      `;

      if (record.weight) html += `<p><strong>Weight:</strong> ${record.weight} kg</p>`;

      // PDF link
      if (record.pdf_base64) {
        html += `<p><a href="${record.pdf_base64}" download="Batch_${record.batch_id}.pdf">Download PDF</a></p>`;
      }

      // Image
      if (record.image_base64) {
        html += `<img src="${record.image_base64}" class="batch-image" alt="Batch Image">`;
      }

      stepBox.innerHTML = html;
      container.appendChild(stepBox);

      // Add arrow if not last
      if (index < history.length - 1) {
        const arrow = document.createElement('div');
        arrow.classList.add('arrow');
        arrow.textContent = "➡️";
        container.appendChild(arrow);
      }
    });

  } catch (err) {
    container.innerHTML = `Error loading batch history: ${err.message}`;
    console.error(err);
  }
});
