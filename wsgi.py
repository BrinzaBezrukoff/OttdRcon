from app import app, scheduler, sessions_manager
import views
import ottd


scheduler.start()

if __name__ == '__main__':
    app.run(debug=True, host="192.168.2.43")
