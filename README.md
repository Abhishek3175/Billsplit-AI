# 🍽️ BillSplit AI

A full-stack web application that uses AI to extract item-wise details from restaurant bills and calculate individual shares based on consumed items, including proportional tax distribution.

## ✨ Features

- **AI-Powered Bill Processing**: Upload a restaurant bill image and let OpenAI's GPT-4 Vision extract structured data
- **Smart Item Extraction**: Automatically identifies items, quantities, prices, taxes, and totals
- **Individual Share Calculation**: Select your consumed items and get your exact share including proportional tax
- **Modern UI/UX**: Beautiful, responsive interface with drag-and-drop file upload
- **Real-time Processing**: Instant calculations with visual feedback

## 🛠️ Tech Stack

### Backend
- **Flask**: Python web framework
- **Google Gemini API**: Gemini 1.5 Flash Vision for image processing
- **MySQL**: Database for storing bill data
- **Flask-SQLAlchemy**: Database ORM
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client for API calls
- **CSS3**: Modern styling with gradients and animations

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Google Gemini API key

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Splitbill
```

### 2. Backend Setup

#### Create and Activate Virtual Environment

```bash
cd backend
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Environment Configuration

Copy the environment template and configure your settings:

```bash
cp env_template.txt .env
```

Edit `.env` with your actual values:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Database Configuration
DATABASE_URL=mysql://username:password@localhost/billsplit_db

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

#### Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE billsplit_db;
```

2. Update the `DATABASE_URL` in your `.env` file with your MySQL credentials.

#### Run the Backend

```bash
python app.py
```

The Flask server will start on `http://localhost:5000`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Run Development Server

```bash
npm run dev
```

The React app will start on `http://localhost:3000`

## 📱 Usage

1. **Upload Bill**: Drag and drop or click to upload a restaurant bill image
2. **AI Processing**: Wait for the AI to extract bill details
3. **Review Items**: Check the extracted items and their details
4. **Select Your Items**: Click on the items you consumed
5. **Calculate Share**: Click "Calculate My Share" to get your total
6. **View Breakdown**: See your item subtotal, tax share, and final total

## 🔧 API Endpoints

### POST `/upload-bill`
Upload a bill image for AI processing.

**Request**: Multipart form data with `image` field
**Response**: JSON with extracted bill data and bill ID

### POST `/calculate-share`
Calculate individual share based on consumed items.

**Request**: JSON with `bill_id` and `consumed_items` array
**Response**: JSON with user's share breakdown

### GET `/bills`
Retrieve all processed bills.

### GET `/bills/<id>`
Retrieve a specific bill by ID.

## 🗄️ Database Schema

The application creates a `Bill` table with the following structure:

- `id`: Primary key
- `bill_date`: Date of the bill
- `vendor`: Restaurant/store name
- `subtotal`: Bill subtotal
- `tax`: Tax amount
- `total`: Total bill amount
- `currency`: Currency code
- `items_json`: JSON string of items array
- `created_at`: Timestamp of creation

## 🎨 Customization

### Styling
- Modify CSS files in `frontend/src/components/` to customize the appearance
- Update color schemes in `frontend/src/App.css`

### AI Processing
- Adjust the prompt in `backend/app.py` to modify how the AI extracts information
- Change the OpenAI model in the API call if needed

## 🚨 Important Notes

- **API Key Security**: Never commit your `.env` file to version control
- **Image Quality**: Higher quality images yield better extraction results
- **File Size**: Maximum image size is 10MB
- **Supported Formats**: JPEG, PNG, and other common image formats
- **Gemini API**: Requires Google AI Studio API key with Gemini 1.5 Flash access

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify MySQL is running
   - Check database credentials in `.env`
   - Ensure database exists

2. **Gemini API Error**
   - Verify API key is correct
   - Check API key has sufficient credits
   - Ensure Gemini 1.5 Flash access

3. **Frontend Build Issues**
   - Clear `node_modules` and reinstall
   - Check Node.js version compatibility

4. **CORS Issues**
   - Verify backend is running on port 5000
   - Check Vite proxy configuration

## 📈 Future Enhancements

- [ ] User authentication and bill history
- [ ] Multiple bill splitting scenarios
- [ ] Export functionality (PDF, CSV)
- [ ] Mobile app
- [ ] Integration with payment apps
- [ ] Bill analytics and spending insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google for providing the Gemini Vision API
- The Flask and React communities for excellent documentation
- Contributors and users of this project

---

**Happy Bill Splitting! 🎉**
