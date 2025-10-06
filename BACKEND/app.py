from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import io
import timm
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Model configuration
MODEL_PATH = 'deepfake_vit_final.pth'
NUM_CLASSES = 2  # Real and Fake

# Define the custom model architecture
class DeepfakeViT(nn.Module):
    def __init__(self, num_classes=2):
        super(DeepfakeViT, self).__init__()
        # Load pretrained ViT
        self.vit = timm.create_model('vit_tiny_patch16_224', pretrained=False)
        
        # Get the number of features from ViT
        num_features = self.vit.head.in_features
        
        # Remove the original head
        self.vit.head = nn.Identity()
        
        # Custom classifier - matching the saved model indices
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),           # index 0
            nn.Linear(num_features, 512),  # index 1
            nn.ReLU(),                 # index 2
            nn.Dropout(0.3),           # index 3
            nn.Linear(512, num_classes)    # index 4
        )
    
    def forward(self, x):
        x = self.vit(x)
        x = self.classifier(x)
        return x

# Load the model
def load_model():
    try:
        # Create the custom ViT model
        model = DeepfakeViT(num_classes=NUM_CLASSES)
        
        # Load the trained weights
        checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=False)
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict):
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
            elif 'state_dict' in checkpoint:
                model.load_state_dict(checkpoint['state_dict'])
            else:
                model.load_state_dict(checkpoint)
        else:
            model.load_state_dict(checkpoint)
        
        model = model.to(device)
        model.eval()
        print(f"Model loaded successfully on {device}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return None

# Initialize model
model = load_model()

# Image preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def preprocess_image(image_bytes):
    """Preprocess the image for model input"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply transforms
        img_tensor = transform(img)
        img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension
        
        return img_tensor
    except Exception as e:
        raise Exception(f"Error preprocessing image: {e}")

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Deepfake Detection API is running',
        'model_loaded': model is not None,
        'device': str(device)
    })

@app.route('/predict', methods=['POST'])
@app.route('/api/detect', methods=['POST'])  # Alternative endpoint
def predict():
    """Predict if an image is real or fake"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please check the model path.'
        }), 500
    
    # Check if image is in the request
    if 'image' not in request.files:
        return jsonify({
            'error': 'No image provided. Please upload an image file.'
        }), 400
    
    file = request.files['image']
    
    # Check if file is empty
    if file.filename == '':
        return jsonify({
            'error': 'No image selected.'
        }), 400
    
    try:
        # Read image bytes
        img_bytes = file.read()
        
        # Preprocess image
        img_tensor = preprocess_image(img_bytes)
        img_tensor = img_tensor.to(device)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            # Get probabilities for both classes
            fake_prob = probabilities[0][0].item()
            real_prob = probabilities[0][1].item()
        
        # Prepare response
        result = {
            'prediction': 'Real' if predicted.item() == 1 else 'Fake',
            'confidence': float(confidence.item()),
            'probabilities': {
                'fake': float(fake_prob),
                'real': float(real_prob)
            },
            'class_id': int(predicted.item())
        }
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error processing image: {str(e)}'
        }), 500

@app.route('/predict_base64', methods=['POST'])
def predict_base64():
    """Predict using base64 encoded image"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please check the model path.'
        }), 500
    
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({
                'error': 'No image data provided.'
            }), 400
        
        # Decode base64 image
        img_data = base64.b64decode(data['image'])
        
        # Preprocess image
        img_tensor = preprocess_image(img_data)
        img_tensor = img_tensor.to(device)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            fake_prob = probabilities[0][0].item()
            real_prob = probabilities[0][1].item()
        
        result = {
            'prediction': 'Real' if predicted.item() == 1 else 'Fake',
            'confidence': float(confidence.item()),
            'probabilities': {
                'fake': float(fake_prob),
                'real': float(real_prob)
            },
            'class_id': int(predicted.item())
        }
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error processing image: {str(e)}'
        }), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Predict multiple images at once"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please check the model path.'
        }), 500
    
    if 'images' not in request.files:
        return jsonify({
            'error': 'No images provided.'
        }), 400
    
    files = request.files.getlist('images')
    
    if len(files) == 0:
        return jsonify({
            'error': 'No images selected.'
        }), 400
    
    results = []
    
    for idx, file in enumerate(files):
        try:
            img_bytes = file.read()
            img_tensor = preprocess_image(img_bytes)
            img_tensor = img_tensor.to(device)
            
            with torch.no_grad():
                outputs = model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
                
                fake_prob = probabilities[0][0].item()
                real_prob = probabilities[0][1].item()
            
            results.append({
                'filename': file.filename,
                'prediction': 'Real' if predicted.item() == 1 else 'Fake',
                'confidence': float(confidence.item()),
                'probabilities': {
                    'fake': float(fake_prob),
                    'real': float(real_prob)
                }
            })
        except Exception as e:
            results.append({
                'filename': file.filename,
                'error': str(e)
            })
    
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)