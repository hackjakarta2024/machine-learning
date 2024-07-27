from initCourseGeneration import InitCourseRecommendation
from CourseRecommender import CourseRecommendation
from flask import Flask, request, jsonify
import os
import json
import pandas as pd

app = Flask(__name__)

PROJECT_ID = "bytes-prototype"
REGION = "us-central1"
DATASET = "bytes_course_sources"
TABLE = "web_research"
POSTGRE_DATASET = 'bytes-postgre'
POSTGRE_TABLE = 'user_topic_like'

@app.route('/initcourse', methods=['POST'])
def get_initcourse():
    data = str(request.json).replace("'", '"')
    req = json.loads(data)
    course_recommendation = InitCourseRecommendation(req, PROJECT_ID, DATASET, TABLE, REGION)
    rec = course_recommendation.generate_recommendation()
    return jsonify(rec)

@app.route('/recommendation', methods=['POST'])
def get_recommendation():
    data = str(request.json).replace("'", '"')
    req = json.loads(data)
    course_recommendation = CourseRecommendation(req, PROJECT_ID, DATASET, TABLE, REGION)
    df = course_recommendation.query_from_bq(PROJECT_ID, REGION, POSTGRE_DATASET, POSTGRE_TABLE)
    rec = course_recommendation.generate_recommendation(df, req['userId'])
    return jsonify(rec)

if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)) )