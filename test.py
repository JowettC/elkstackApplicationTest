from flask import Flask
from random import randint
import time

app = Flask(__name__)
@app.route('/successful', methods=['GET'])
def test1():
    # app.logger.info('Successful logging')
    return "Successful logging!"


@app.route('/unsuccessful', methods=['GET'])
def test2():
    # app.logger.info('Unsuccessful logging')
    return "Unsuccessful logging!",400
    
@app.route('/long/successful', methods=['GET'])
def test3():
    # app.logger.info('Unsuccessful logging')
    time.sleep(5)
    return "5 second wait successful"

@app.route('/random', methods=['GET'])
def test4():
    # app.logger.info('Unsuccessful logging')
    value = randint(0,10)
    if value > 5:
        return "Successful logging!"
    else:
        return "Unsuccessful logging!",400

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True)