⚽ Score Tracking System
This project is a system that retrieves match scores via an API and instantly transmits match information about the teams determined by the users. 
Messaging infrastructure was established with RabbitMQ, and the user interface was prepared with CustomTkinter.

🚀 Features
- Retrieves past match scores via API.
- Sends score notifications for specific teams via RabbitMQ.
- The user receives only the relevant matches by entering the team name from the terminal interface.
- Live scores are reflected on the screen with the CustomTkinter interface.

🔧 Installation

1. Clone this project:
   ```bash
git clone https://github.com/MerveKaracicek/Score_Tracking_System.git

cd score-tracking-system

2. Install the required libraries:
pip install -r requirements.txt

3.Create the .env file and enter your API key in it:
API_KEY=YOUR_API_KEY

🛠 Technologies Used
- Python
- RabbitMQ
- CustomTkinter (GUI)
- API-Football (spor verisi)

 🖼️ Example of GUI 
 
![Ekran görüntüsü 2025-06-19 211207](https://github.com/user-attachments/assets/fc2315bc-c83a-453a-9436-79079c1324d1)

