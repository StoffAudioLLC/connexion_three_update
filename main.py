"""
A script to test functionality
"""
import connexion
from ratelimiter import RateLimiter

app = connexion.App("Connexion_Test_App")

app.add_api('swagger.yaml')

def TooManyRequests() -> tuple:
    return "Ratelimit reached, try again later", 425

@RateLimiter(max_calls=10, period=1, callback=TooManyRequests())
def hello():
    return "Hello", 200

if __name__ == '__main__':
    app.run(port=8893)
    