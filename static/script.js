function downloadImage(url) {
    const link = document.createElement('a');
    link.href = url;
    link.download = 'decoded.png';
    link.click();
  }
  

document.getElementById('upload-form-text').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const form = event.target;
    const formData = new FormData(form);
  
    fetch('/upload-text', {
      method: 'POST',
      body: formData,
    })
    .then(response => response.text())
    .then(text => {
      document.getElementById('response').innerText = text;
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
  


document.getElementById('upload-form-HostImg').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.text())
    .then(text => {
        document.getElementById('response').innerText = text;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('upload-form-SecImg').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch('/upload_sec', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.text())
    .then(text => {
        document.getElementById('response').innerText = text;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});






document.getElementById('encode-button_txt').addEventListener('click', function() {
    const encodingKey = document.getElementById('encoding-key').value;
    const data = JSON.stringify({ encoding_key: encodingKey });

    fetch('/encode_txt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('La réponse du serveur n\'est pas OK.');
        }
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'encoded.png';
        a.click();
    })
    .catch(error => {
        console.error('Error:', error);
        });
});



document.getElementById('encode-button_img').addEventListener('click', function() {
    const encodingKey = document.getElementById('encoding-key').value;
    const data = JSON.stringify({ encoding_key: encodingKey });

    fetch('/encode_img', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    })
    .then(response => {
        if (response.ok) {
        return response.blob();
        } else {
        throw new Error('La réponse du serveur n est pas OK.');
        }
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'encoded.png';
        a.click();
    })

    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('encode-button_img').addEventListener('click', function() {
    const encodingKey = document.getElementById('encoding-key').value;
    const data = JSON.stringify({ encoding_key: encodingKey });

    fetch('/get_output', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('La réponse du serveur n est pas OK.');
        }
    })
    .then(data => {
        const outputElement = document.getElementById('output');
        outputElement.textContent = data.output;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});



// DECODING PART
document.getElementById('upload-form-CodedImg').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch('/upload_coded', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.text())
    .then(text => {
        document.getElementById('response-decoding').innerText = text;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});







// Boutton Récupérer du Texte
document.getElementById('decode-button_txt').addEventListener('click', function() {
    const decodingKey = document.getElementById('decoding-key').value;
    const data = JSON.stringify({ 'decoding-key': decodingKey });

    fetch('/decode_txt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('La réponse du serveur n\'est pas OK.');
        }
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'decoded.txt';
        a.click();
    })
    .catch(error => {
        console.error('Error:', error);
     });
});





// Boutton Récupérer une Image
document.getElementById('decode-button_img').addEventListener('click', function() {
    const decodingKey = document.getElementById('decoding-key').value;
    const data = JSON.stringify({ 'decoding-key': decodingKey });

    fetch('/decode_img', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('La réponse du serveur n\'est pas OK.');
        }
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'decoded.png';
        a.click();
    })
    .catch(error => {
        console.error('Error:', error);
     });
});

