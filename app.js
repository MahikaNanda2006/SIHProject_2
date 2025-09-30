document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("packagingForm");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const stageId = document.getElementById("stageId").value;
    const endReportFile = document.getElementById("endReport").files[0];
    if (!stageId || !endReportFile) {
      alert("Please fill all fields.");
      return;
    }

    const formData = new FormData();
    formData.append("parent_batch_id", stageId);
    formData.append("stakeholder", "packaging");
    formData.append("weight", "100kg");
    formData.append("report", endReportFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/submit/packaging", {
        method: "POST",
        body: formData,
      });

      // Get response text then JSON-safe parse (robust)
      const text = await response.text();
      let data = {};
      try { data = text ? JSON.parse(text) : {}; } catch (err) { console.warn("Response not JSON:", text); data = { raw: text }; }

      console.log("Backend response object:", data);

      if (!response.ok) {
        alert("Backend error: " + (data.detail || response.status || text));
        return;
      }

      // Get batch id robustly (support multiple backends)
      const batchId = data.batch_id ?? data.batchId ?? (typeof data === "string" ? data : null);

    if (!batchId) {
    alert("No batch_id found in backend response. See console for details.");
    console.log("Full response:", data);
    return;
    }

    // ✅ use the variable, not the string
    window.location.href = `qr.html?batch_id=${encodeURIComponent(batchId)}`;

    } catch (err) {
      console.error(err);
      alert("Failed to submit batch. Check console for details.");
    }
  });
});
