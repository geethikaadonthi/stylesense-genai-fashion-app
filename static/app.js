const recommendForm = document.getElementById("recommend-form");
const imageForm = document.getElementById("image-form");

const recommendationOutput = document.getElementById("recommendation-output");
const imageOutput = document.getElementById("image-output");

const printList = (items) => `<ul>${items.map((item) => `<li>${item}</li>`).join("")}</ul>`;

recommendForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    style: recommendForm.style.value,
    occasion: recommendForm.occasion.value,
    weather: recommendForm.weather.value,
    budget: recommendForm.budget.value,
  };

  const response = await fetch("/api/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  recommendationOutput.innerHTML = `
    <p><strong>Styling Advice:</strong> ${data.styling_advice}</p>
    <p><strong>Outfits:</strong></p>
    ${printList(data.outfit_recommendations)}
    <p><strong>Trend Signals:</strong></p>
    ${printList(data.trend_notes)}
  `;
});

imageForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(imageForm);
  const response = await fetch("/api/analyze-image", {
    method: "POST",
    body: formData,
  });
  const data = await response.json();

  imageOutput.innerHTML = `
    <p><strong>Image Summary:</strong> ${data.image_summary}</p>
    <p><strong>Matched Styles:</strong></p>
    ${printList(data.matched_styles)}
    <p><strong>Improvement Tips:</strong></p>
    ${printList(data.improvement_tips)}
  `;
});
