# Telex.im AI Code Helper Agent

A FastAPI-based backend service that provides AI-powered code reviews and explanations through the Telex.im platform.

## Features

- **Code Review**: Get AI-powered code reviews with suggestions for improvements
- **Code Explanation**: Understand complex code with detailed explanations
- **Q&A**: Ask questions about your code and get helpful answers
- **Webhook Integration**: Seamless integration with Telex.im platform
- **RESTful API**: Well-documented endpoints for easy integration

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Mistral AI API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Fast_agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Mistral AI API key:
   ```env
   MISTRAL_API_KEY=your_api_key_here
   MISTRAL_MODEL=mistral-small-latest  # Optional: specify model
   ```

## Running the Application

### Development

```bash
uvicorn app.main:app --reload --port 8080
```

The API will be available at `http://localhost:8080`

### Production

For production, use a production ASGI server like uvicorn with gunicorn:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## API Endpoints

- `GET /`: Health check endpoint
- `POST /webhook`: Main webhook endpoint for Telex.im integration
- `GET /test-llm`: Test endpoint to verify LLM connection

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MISTRAL_API_KEY` | Yes | - | Your Mistral AI API key |
| `MISTRAL_MODEL` | No | mistral-small-latest | The Mistral model to use |

## Project Structure

```
Fast_agent/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and routes
│   ├── schemas.py        # Pydantic models
│   ├── exceptions.py     # Custom exceptions and handlers
│   └── agent/
│       └── core.py       # Core LLM integration logic
├── .env.example         # Example environment variables
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error messages in the following format:

```json
{
  "success": false,
  "error": "Error message",
  "details": {
    "additional_info": "More details about the error"
  }
}
```

## Testing

To test the LLM connection:

```bash
curl http://localhost:8080/test-llm
```

## Deployment

### Docker

1. Build the Docker image:
   ```bash
   docker build -t telex-ai-agent .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:80 --env-file .env telex-ai-agent
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Mistral AI](https://mistral.ai/)
- [Telex.im](https://telex.im/)
