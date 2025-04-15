const imageElement = document.getElementById('myImage');
const loadingElement = document.getElementById('loading');
const fileInput = document.getElementById('fileInput');

// Afficher l'image immédiatement après sélection
fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  
  if (file) {
    const reader = new FileReader();
    loadingElement.style.display = 'block'; // Affiche "Chargement..."
    
    reader.onload = (e) => {
      imageElement.src = e.target.result;
      imageElement.style.display = 'block';
      loadingElement.style.display = 'none'; // Cacher "Chargement..."
    };
    
    reader.readAsDataURL(file); // Lire le fichier image
  }
});
