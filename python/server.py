from flask import Flask, request, send_from_directory, jsonify

app = Flask(__name__)


@app.after_request
def after(response):
    if request.method == "GET":
        response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/weeby/<path:path>', methods=['GET'])
def send_css(path):
    print (path)
    return send_from_directory('weeby', path)


@app.route('/weeby/flappy', methods=['POST'])
def flappy():
    json = request.json
    walls = json['walls']
    player = json['me']
    base_time = player['x'] / 4  # get the timestamp
    # find a wall
    i = 0
    print(walls)
    if len(walls) > 0:
        # get the next wall
        while (walls[i]['x'] + 50 - player['x']) < 0:
            i += 1
    next_wall = walls[i]
    wall_distance = next_wall['x'] - player['x']
    print("wall_distance ==>", wall_distance)
    # find the gap
    if abs(wall_distance) > 55:
        #  upper
        if player['y'] >= (walls[i]['gaps'][0]['y'] + 135):
            queue = []
        # in the middle
        elif walls[i]['gaps'][0]['y'] < player['y'] < (walls[i]['gaps'][0]['y'] + 135):
            #  upper acc
            if player['vy'] >= 0:
                queue = []
            # down acc
            else:
                if (player['y'] - walls[i]['gaps'][0]['y']) < 10:
                    queue = [base_time + 1]
                else:
                    queue = []
        # down
        elif walls[i]['gaps'][0]['y'] >= player['y']:
            queue = [base_time + 1]
        else:
            queue = []

    # pass the gap
    else:
        # lower than gap
        if player['y'] < walls[i]['gaps'][0]['y'] - 10:
            queue = [base_time + 1]
        # almost hit
        elif (player['y'] - walls[i]['gaps'][0]['y']) < 36:
            if player['vy'] <= 0:
                queue = [base_time + 2]
            else:
                queue = []
        else:
            queue = []

    if len(queue) > 0:
        next_time = queue[-1] + 2
    else:
        next_time = base_time + 2
    return jsonify(queue=queue, next=next_time)


@app.route("/weeby/magic", methods=['GET'])
def convert_spell():
    words_map = {'qux': 'baz',
                 'baz': 'bar',
                 'bar': 'qux'}
    magic_words = request.args.get('spell')
    if (len(magic_words) % 3) == 0:  # check if it is a good string
        counter_spell = ''
        for i in range(0, len(magic_words), 3):
            if words_map.get(magic_words[i:i + 3]):  # check if word in dictionary
                counter_spell += words_map.get(magic_words[i:i + 3])
            else:
                return 'cant find the counterspell'
        return counter_spell
    return 'fail not a legal String'


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=1337)
