from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/process_video', methods=['GET'])
def process_video():
    try:
        # Run the command to process the video
        command = [
            'python3', 'people_counter.py',
            '--prototxt', 'detector/MobileNetSSD_deploy.prototxt',
            '--model', 'detector/MobileNetSSD_deploy.caffemodel',
            '--input', 'utils/data/tests/test_1.mp4'
        ]
        subprocess.run(command, check=True)
        
        # Read the total counts from the JSON file
        with open('final_counts.json', 'r') as file:
            counts = json.load(file)
            total_people_inside = counts.get('total_people_inside', 0)

        # Return the people count along with the success message
        return jsonify({
            'message': 'Video processing started successfully.',
            'total_people_inside': total_people_inside
        }), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f"Command '{e.cmd}' returned non-zero exit status {e.returncode}."}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
