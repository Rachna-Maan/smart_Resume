async function analyzeResume() {
  const fileInput = document.getElementById("resumeFile");
  if (!fileInput.files.length) {
    alert("Please upload a file");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData
    });
    const data = await response.json();

    const resultDiv = document.getElementById("result");
    if (data.status === "success") {
      resultDiv.innerHTML = `
        <h4>Resume Score: ${data.score}%</h4>
        <p><strong>Found Skills:</strong> ${data.found_skills.join(", ")}</p>
        <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ")}</p>
        <p><strong>Suggestions:</strong></p>
        <ul>${data.suggestions.map(s => `<li>${s}</li>`).join("")}</ul>
      `;
    } else {
      resultDiv.innerHTML = `<p class="text-danger">${data.message}</p>`;
    }
  } catch (error) {
    document.getElementById("result").innerHTML = `<p class="text-danger">Error: ${error}</p>`;
  }
}