from flask import Flask, request, send_from_directory, make_response, session, send_file
import os
import subprocess
import sys
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['UPLOAD_FOLDER_TXT'] = 'uploads_txt'
app.config['UPLOAD_FOLDER_IMGSEC'] = 'uploads_sec'
app.config['UPLOAD_FOLDER_CODED'] = 'uploads_coded'
app.config['SECRET_KEY'] = 'Cqw90'  

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])    

if not os.path.exists(app.config['UPLOAD_FOLDER_TXT']):
    os.makedirs(app.config['UPLOAD_FOLDER_TXT'])
    
if not os.path.exists(app.config['UPLOAD_FOLDER_IMGSEC']):
    os.makedirs(app.config['UPLOAD_FOLDER_IMGSEC'])

if not os.path.exists(app.config['UPLOAD_FOLDER_CODED']):
    os.makedirs(app.config['UPLOAD_FOLDER_CODED'])
 


@app.route('/') # associer une fonction Python à une URL
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'templates/index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return make_response('Aucune image n\'a été sélectionnée.', 400)

    file = request.files['image']

    if file.filename == '':
        return make_response('Aucune image n\'a été sélectionnée.', 400)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Stockez le nom de fichier de l'image téléchargée dans une variable de session
    session['uploaded_image'] = file.filename

    return 'L\'image Hôte a été téléchargée avec succès.'




@app.route('/upload_sec', methods=['POST'])
def upload_imageSec():
    if 'image' not in request.files:
        return make_response('Aucune image n\'a été sélectionnée.', 400)

    file = request.files['image']

    if file.filename == '':
        return make_response('Aucune image n\'a été sélectionnée.', 400)

    file_path = os.path.join(app.config['UPLOAD_FOLDER_IMGSEC'], file.filename)
    file.save(file_path)

    # Stockez le nom de fichier de l'image téléchargée dans une variable de session
    session['uploaded_imageSec'] = file.filename

    return 'L\'image Secrete a été téléchargée avec succès.'








@app.route('/upload-text', methods=['POST'])
def upload_text():
    if 'text' not in request.files:
        return make_response('Aucun fichier texte n\'a été sélectionné.', 400)

    file = request.files['text']

    if file.filename == '':
        return make_response('Aucun fichier texte n\'a été sélectionné.', 400)

    file_path = os.path.join(app.config['UPLOAD_FOLDER_TXT'], file.filename)
    file.save(file_path)

    session['uploaded_text'] = file.filename

    return 'Le fichier texte a été téléchargé avec succès.'





@app.route('/encode_txt', methods=['POST'])
def encode_txt():
    try:
        uploaded_image = session.get('uploaded_image')
        uploaded_text = session.get('uploaded_text')

        if not uploaded_image or not uploaded_text:
            return 'Aucune image ou fichier texte n\'a été téléchargé.'

        data_path_image = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image)
        data_path_text = os.path.join(app.config['UPLOAD_FOLDER_TXT'], uploaded_text)

        result = subprocess.run(['code_prog_txt.exe', data_path_image, data_path_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            decoded_txt_path = 'coded.png'
            return send_file(decoded_txt_path, mimetype='image/png', as_attachment=True)

        else:
            return f'L\'encodage failed.'

    except Exception as e:
        return f'Erreur lors de l\'encodage : {str(e)}'



@app.route('/encode_img', methods=['POST'])
def encode_img():
    uploaded_image = session.get('uploaded_image')
    uploaded_imageSec = session.get('uploaded_imageSec')

    data = request.get_json()
    encoding_key = data.get('encoding_key')

    if not uploaded_image or not uploaded_imageSec:
        return 'Aucune image ou fichier texte n\'a été téléchargé.'

    data_path_image = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image)
    data_path_imageSec = os.path.join(app.config['UPLOAD_FOLDER_IMGSEC'], uploaded_imageSec)


    result = subprocess.run(['code_prog_imgRGBA.exe', data_path_image, data_path_imageSec, str(encoding_key)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        encoded_image_path = 'coded.png'
        return send_file(encoded_image_path, mimetype='image/png', as_attachment=True)
    else:
        return f"L'encodage n'a pas réussi."
    

@app.route('/get_output', methods=['POST'])
def get_output():
    uploaded_image = session.get('uploaded_image')
    uploaded_imageSec = session.get('uploaded_imageSec')

    if not uploaded_image or not uploaded_imageSec:
        return 'Aucune image ou fichier texte n\'a été téléchargé.'

    data_path_image = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image)
    data_path_imageSec = os.path.join(app.config['UPLOAD_FOLDER_IMGSEC'], uploaded_imageSec)

    result = subprocess.run(['code_prog_imgRGBA_img.exe', data_path_image, data_path_imageSec], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        output = result.stdout.decode('utf-8')
        return {'output': output}
    else:
        return {'error': 'L\'encodage n\'a pas réussi.'}




# ###### DECODING PART ###### #

@app.route('/upload_coded', methods=['POST'])
def upload_coded_image():
    if 'image' not in request.files:
        return make_response('Aucune image n\'a été sélectionnée.', 400)

    file = request.files['image']

    if file.filename == '':
        return make_response('Aucune image n\'a été sélectionnée.', 400)

    file_path = os.path.join(app.config['UPLOAD_FOLDER_CODED'], file.filename)
    file.save(file_path)

    # Stockez le nom de fichier de l'image téléchargée dans une variable de session
    session['uploaded_coded_image'] = file.filename

    return 'L\'image a été téléchargée avec succès.'




@app.route('/decode_txt', methods=['POST'])
def decode_txt():
    try:
        uploaded_image = session.get('uploaded_coded_image')

        data = request.get_json()
        decoding_key = data.get('decoding-key')

        if not uploaded_image:
            return 'Aucune image ou fichier texte n\'a été téléchargé.'

        data_path_image = os.path.join(app.config['UPLOAD_FOLDER_CODED'], uploaded_image)

        result = subprocess.run(['decode_prog_txt.exe', data_path_image], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            decoded_txt_path = 'decoded.txt'
            return send_file(decoded_txt_path, mimetype='text/plain', as_attachment=True)
            
        else:
            return f'L\'encodage failed.'
    except Exception as e:
        return f'Erreur lors du décodage : {str(e)}'


@app.route('/decode_img', methods=['POST'])
def decode_img():
    uploaded_image = session.get('uploaded_coded_image')
    
    data = request.get_json()
    decoding_key = data.get('decoding-key')

    if not uploaded_image:
        return 'Aucune image ou fichier texte n\'a été téléchargé.'

    data_path_image = os.path.join(app.config['UPLOAD_FOLDER_CODED'], uploaded_image)

    result = subprocess.run(['decode_prog_imgRGBA.exe', data_path_image, str(decoding_key)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    if result.returncode == 0:
        decoded_image_path = 'decoded.png'
        return send_file(decoded_image_path, mimetype='image/png', as_attachment=True)
        
    else:
        return f'L\'encodage failed.'




if __name__ == '__main__':
    app.run(debug=True)