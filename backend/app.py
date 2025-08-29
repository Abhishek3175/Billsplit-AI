from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import base64
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost/billsplit_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Configure Google Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Database Models
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_date = db.Column(db.String(50), nullable=True)
    vendor = db.Column(db.String(255), nullable=True)
    subtotal = db.Column(db.Float, nullable=True)
    tax = db.Column(db.Float, nullable=True)
    total = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), default='USD')
    items_json = db.Column(db.Text, nullable=True)  # Store items as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'bill_date': self.bill_date,
            'vendor': self.vendor,
            'subtotal': self.subtotal,
            'tax': self.tax,
            'total': self.total,
            'currency': self.currency,
            'items': json.loads(self.items_json) if self.items_json else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Routes
@app.route('/upload-bill', methods=['POST'])
def upload_bill():
    try:
        print("=== Starting bill upload process ===")  # Debug log
        
        if 'image' not in request.files:
            print("No image file in request")  # Debug log
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            print("Empty filename")  # Debug log
            return jsonify({'error': 'No image file selected'}), 400
        
        print(f"Processing image: {file.filename}")  # Debug log
        
        # Convert image to base64
        image_data = file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        print(f"Image converted to base64, length: {len(base64_image)}")  # Debug log
        
        # Prepare prompt for Gemini
        prompt = """
        Analyze this restaurant bill image and extract the information into a JSON object with exactly this structure:
        {
            "bill_date": "date of the bill",
            "vendor": "restaurant/store name",
            "items": [
                {
                    "name": "item name",
                    "quantity": quantity_as_number,
                    "price": price_as_number
                }
            ],
            "subtotal": subtotal_as_number,
            "tax": tax_amount_as_number,
            "total": total_amount_as_number,
            "currency": "currency_code"
        }
        
        IMPORTANT: 
        - Return ONLY the JSON object, no additional text
        - All monetary values must be numbers (not strings)
        - Quantities must be integers
        - Include all items with their names, quantities, and prices
        - Calculate subtotal as sum of (quantity × price) for all items
        - Extract tax amount and total from the bill
        """
        
        # Call Google Gemini API
        try:
            print("Initializing Gemini model...")  # Debug log
            
            # Use simple model initialization
            model = genai.GenerativeModel('gemini-1.5-flash')
            print("Gemini model initialized successfully")  # Debug log
            
            # Prepare the image data for Gemini
            print("Preparing image data...")  # Debug log
            image_data_bytes = base64.b64decode(base64_image)
            print(f"Image data prepared, size: {len(image_data_bytes)} bytes")  # Debug log
            
            # Create the prompt with image
            print("Sending request to Gemini API...")  # Debug log
            response = model.generate_content([
                prompt,
                {"mime_type": "image/jpeg", "data": image_data_bytes}
            ])
            print("Received response from Gemini API")  # Debug log
            
            # Check if response was blocked
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                print(f"Content blocked: {response.prompt_feedback.block_reason}")  # Debug log
                return jsonify({'error': f'Content blocked: {response.prompt_feedback.block_reason}'}), 400
            
            # Check if response generation failed
            if not response.text:
                print("Empty response from Gemini")  # Debug log
                return jsonify({'error': 'Gemini API returned empty response'}), 500
            
            # Extract the response text
            content = response.text
            print(f"Gemini Response: {content}")  # Debug log
            
            # Clean the response to extract JSON
            print("Extracting JSON from response...")  # Debug log
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            print(f"JSON start index: {start_idx}, end index: {end_idx}")  # Debug log
            
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                print(f"Extracted JSON string: {json_str}")  # Debug log
                try:
                    extracted_data = json.loads(json_str)
                    print("JSON parsed successfully")  # Debug log
                except json.JSONDecodeError as json_error:
                    print(f"JSON parsing error: {json_error}")  # Debug log
                    return jsonify({'error': f'Failed to parse JSON response: {json_error}'}), 500
            else:
                print(f"No JSON found in response. Content: {content}")  # Debug log
                return jsonify({'error': 'Failed to extract structured data from image. No JSON found in response.'}), 500
                
        except Exception as gemini_error:
            error_msg = str(gemini_error)
            print(f"Gemini API Error: {error_msg}")  # Debug log
            print(f"Error type: {type(gemini_error)}")  # Debug log
            
            # Handle specific network errors
            if "timeout" in error_msg.lower() or "dns" in error_msg.lower():
                return jsonify({
                    'error': 'Network connection issue. Please check your internet connection and try again.',
                    'details': error_msg
                }), 503
            elif "api key" in error_msg.lower() or "authentication" in error_msg.lower():
                return jsonify({
                    'error': 'Invalid API key. Please check your Gemini API key configuration.',
                    'details': error_msg
                }), 401
            elif "model" in error_msg.lower() or "generative" in error_msg.lower():
                return jsonify({
                    'error': 'Model initialization failed. Please try again.',
                    'details': error_msg
                }), 500
            else:
                return jsonify({'error': f'Gemini API error: {error_msg}'}), 500
        
        # Validate required fields
        print(f"Extracted data keys: {list(extracted_data.keys())}")  # Debug log
        required_fields = ['items', 'subtotal', 'tax', 'total']
        for field in required_fields:
            if field not in extracted_data:
                print(f"Missing field: {field}")  # Debug log
                return jsonify({'error': f'Missing required field: {field}. Available fields: {list(extracted_data.keys())}'}), 400
        
        print("All required fields found, proceeding to database storage")  # Debug log
        
        # Store in database
        try:
            bill = Bill(
                bill_date=extracted_data.get('bill_date'),
                vendor=extracted_data.get('vendor'),
                subtotal=float(extracted_data['subtotal']),
                tax=float(extracted_data['tax']),
                total=float(extracted_data['total']),
                currency=extracted_data.get('currency', 'USD'),
                items_json=json.dumps(extracted_data['items'])
            )
            
            print("Bill object created, adding to database...")  # Debug log
            db.session.add(bill)
            db.session.commit()
            print(f"Bill saved to database with ID: {bill.id}")  # Debug log
            
        except Exception as db_error:
            print(f"Database error: {db_error}")  # Debug log
            return jsonify({'error': f'Database error: {str(db_error)}'}), 500
        
        # Return the extracted data
        print("Preparing success response...")  # Debug log
        response_data = {
            'success': True,
            'message': 'Bill processed successfully',
            'bill_id': bill.id,
            'data': extracted_data
        }
        print(f"Success response prepared: {response_data}")  # Debug log
        return jsonify(response_data), 200
        
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to parse extracted data'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/calculate-share', methods=['POST'])
def calculate_share():
    try:
        data = request.get_json()
        
        if not data or 'bill_id' not in data or 'consumed_items' not in data:
            return jsonify({'error': 'Missing required fields: bill_id and consumed_items'}), 400
        
        bill_id = data['bill_id']
        consumed_items = data['consumed_items']
        
        # Get bill from database
        bill = Bill.query.get(bill_id)
        if not bill:
            return jsonify({'error': 'Bill not found'}), 404
        
        # Parse items from JSON
        all_items = json.loads(bill.items_json)
        
        # Calculate user's share
        user_subtotal = 0
        for consumed_item in consumed_items:
            # Find the item in the bill
            for bill_item in all_items:
                if (bill_item['name'].lower() == consumed_item['name'].lower() and 
                    bill_item['quantity'] == consumed_item['quantity']):
                    user_subtotal += bill_item['price'] * bill_item['quantity']
                    break
        
        if user_subtotal == 0:
            return jsonify({'error': 'No matching items found'}), 400
        
        # Calculate proportional tax
        tax_ratio = user_subtotal / bill.subtotal
        user_tax_share = tax_ratio * bill.tax
        
        # Calculate total
        user_total = user_subtotal + user_tax_share
        
        return jsonify({
            'user_subtotal': round(user_subtotal, 2),
            'user_tax_share': round(user_tax_share, 2),
            'user_total': round(user_total, 2),
            'currency': bill.currency,
            'bill_total': bill.total
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/bills', methods=['GET'])
def get_bills():
    try:
        bills = Bill.query.order_by(Bill.created_at.desc()).all()
        return jsonify([bill.to_dict() for bill in bills]), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    try:
        bill = Bill.query.get(bill_id)
        if not bill:
            return jsonify({'error': 'Bill not found'}), 404
        return jsonify(bill.to_dict()), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
