# 📅 SIAK-NG to Google Calendar API Integration Project

This project utilizes the **Google Calendar API** and **Selenium** to seamlessly migrate events from the SIAK-NG website to newly created events in Google Calendar.

## 🚀 Getting Started
### Initialization
- Clone the repository.
- Update the `USERNAME` and `PASSWORD` fields in the `userdata.txt` file located in the `config` folder.

### 1️⃣ Prerequisites
- Python 3.x (if using Python)
- Required libraries (install via `requirements.txt`)
- A Google Cloud account

## 🔐 Obtaining the credentials to communicate with Google Calendar
#### 1. Setting Up Google Calendar API

1. **Go to [Google Cloud Console](https://console.cloud.google.com/):**  
   - Create or select an existing project.
   - Navigate to **APIs & Services > Library**.
   - Search for **Google Calendar API** and enable it.

2. **Create Credentials:**  
    - Go to **APIs & Services > Credentials** in Google Cloud Console.
    - Click **Create Credentials** → **Service Account**.
    - Set the service account name to anything and click **Done**.

3. **Generate a Key:**
    ![alt text](https://github.com/saddamtitanio/siak-to-google-calendar/blob/main/docs/1.png)
    - Click the created service account → **Keys** tab → **Add Key** → **Create New Key**.
    - Choose **JSON** format and download the key file.

#### 2. Adding `credentials.json`
   - Place the downloaded JSON file into the root directory of the project and rename it to `credentials.json`.

#### 3. Share Calendar Access
![alt text](https://github.com/saddamtitanio/siak-to-google-calendar/blob/main/docs/image.png)
- Go to [Google Calendar](https://calendar.google.com/).
- Open calendar settings → **Share with specific people**.
- Add the **Service Account email** (found in the JSON key file) with desired permissions.
- Copy the calendar ID in the `Integrate calendar` section into `config/userdata.txt` file
---

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### ▶️ Run the Project
  ```bash
  python main.py
  ```

### Output
![alt text](https://github.com/saddamtitanio/siak-to-google-calendar/blob/main/docs/siak.png)
![alt text](https://github.com/saddamtitanio/siak-to-google-calendar/blob/main/docs/calendar.png)
