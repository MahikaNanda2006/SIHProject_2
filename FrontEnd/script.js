const form = document.getElementById("collectorForm");
const dialog = document.getElementById("confirmationDialog");
const generatedIdEl = document.getElementById("generatedId");
const summaryEl = document.getElementById("summary");
const closeDialogBtn = document.getElementById("closeDialog");
const newCollectionBtn = document.getElementById("newCollection");

function generateUniqueId() {
  const timestamp = Date.now().toString(36);
  const randomStr = Math.random().toString(36).substring(2, 8);
  return `COL-${timestamp}-${randomStr}`.toUpperCase();
}

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const batchId = document.getElementById("batchId").value.trim();
  const speciesName = document.getElementById("speciesName").value.trim();
  const weight = document.getElementById("weight").value.trim();
  const isVerified = document.getElementById("verification").checked;

  if (!batchId || !speciesName || !weight || !isVerified) {
    return;
  }

  const uniqueId = generateUniqueId();
  generatedIdEl.textContent = uniqueId;

  summaryEl.innerHTML = `
    <p><strong>Batch ID:</strong> ${batchId}</p>
    <p><strong>Species:</strong> ${speciesName}</p>
    <p><strong>Weight:</strong> ${weight} kg</p>
  `;

  dialog.classList.remove("hidden");
});

closeDialogBtn.addEventListener("click", () => {
  dialog.classList.add("hidden");
});

newCollectionBtn.addEventListener("click", () => {
  form.reset();
  dialog.classList.add("hidden");
  generatedIdEl.textContent = "";
  summaryEl.innerHTML = "";
});
