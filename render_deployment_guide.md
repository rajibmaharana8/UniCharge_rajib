# Render Deployment Guide: ML Models

To deploy your ML models on Render, you should create two separate **Web Services**. This allows each API to scale independently and have its own URL.

## 1. CPU Prediction API (Flask)

1.  **Log in to Render** and click **New +** > **Web Service**.
2.  **Connect your Repository**: `UniCharge_rajib`.
3.  **Configure the Service**:
    *   **Name**: `unicharge-cpu-prediction`
    *   **Environment**: `Python 3`
    *   **Root Directory**: `ml-engine/models/cpu_prediction`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app`
4.  **Advanced**:
    *   Add an Environment Variable: `PORT` = `10000` (Render usually sets this automatically).

---

## 2. Personalized Wallet API (FastAPI)

1.  **Click New +** > **Web Service**.
2.  **Connect your Repository**: `UniCharge_rajib`.
3.  **Configure the Service**:
    *   **Name**: `unicharge-wallet-prediction`
    *   **Environment**: `Python 3`
    *   **Root Directory**: `ml-engine/models/Personalised_Wallet`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4.  **Advanced**:
    *   Add an Environment Variable: `PORT` = `10000`.

---

## 3. Connecting to your Website (Frontend/Backend)

Once deployed, Render will provide you with two URLs (e.g., `https://unicharge-cpu-prediction.onrender.com`).

### Update your Frontend/Backend:
Replace the local URLs (`http://localhost:5000` or `http://localhost:8000`) with these new Render URLs in your code:

-   **For CPU Prediction**: Use the URL from Service 1.
-   **For Wallet Suggestions**: Use the URL from Service 2.

### Troubleshooting:
-   **Dependencies**: I have already updated `requirements.txt` to include `gunicorn` and `uvicorn` which are needed for Render.
-   **Memory**: If the build fails due to "Out of Memory", you might need to upgrade to a higher Render tier, as ML libraries like `pandas` and `scikit-learn` can be memory-intensive during installation.
