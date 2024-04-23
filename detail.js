const toggleButton = document.getElementById('toggleButton');
const detailSection = document.getElementById('detailSection');

toggleButton.addEventListener('click', function() {
  if (detailSection.style.display === 'none') {
    detailSection.style.display = 'block';
    toggleButton.textContent = 'Đóng chi tiết';
  } else {
    detailSection.style.display = 'none';
    toggleButton.textContent = 'Mở chi tiết';
  }
});
