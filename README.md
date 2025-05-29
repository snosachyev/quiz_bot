# installation

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

# run

    cp .env_template .env
    python3 src/main.py

# bot`s link

    t.me/snosachev_bot

# bot`s comman

    "start" - called on click start button

    "right_answer" -  called when right answer
    "wrong_answer" -  called when wrong answer
    
    "Начать игру" - called on click Начать игру button or type Начать игру
    "quiz" - called on /quiz command
    "Начать игру" and "quiz" usin the same handler

