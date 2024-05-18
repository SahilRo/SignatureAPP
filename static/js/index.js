function generateSignature() {
    const form = document.getElementById('signatureForm');
    const formData = new FormData(form);
    fetch('http://localhost:5000/generate_signature', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const preview = document.getElementById('signaturePreview');
        preview.innerHTML = `<img src="${url}" alt="Signature Preview">`;
        document.getElementById('downloadButton').style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
    }

    function downloadSignature() {
        const img = document.querySelector('#signaturePreview img');
        const url = img.src;
        const a = document.createElement('a');
        a.href = url;
        a.download = 'signature.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
 