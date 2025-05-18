from flask import Flask, request, render_template_string
import math

app = Flask(__name__)

result_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>보정 결과</title>
    <style>
        body { font-family: Arial; padding: 20px; max-width: 600px; margin: auto; text-align: center; }
    </style>
</head>
<body>
    <h1>보정 결과</h1>
    <p><strong>{{ user }}</strong>님의 입력 시간은 {{ input_time }}분이고,</p>
    <p>측정된 거리 {{ distance_km }}km에 대한 <strong>표준 속도 기준 소요시간</strong>은</p>
    <p style="font-size: 1.5em; color: blue;"><strong>{{ corrected_time }}분</strong></p>
    <p><a href="/">다시 입력하기</a></p>
</body>
</html>
"""

@app.route("/adjust_time", methods=["POST"])
def adjust_time():
    user_name = request.form.get("user_name")
    walk_time = float(request.form.get("walk_time"))  # 분 단위

    start_lat = float(request.form.get("start_lat"))
    start_lng = float(request.form.get("start_lng"))
    end_lat = float(request.form.get("end_lat"))
    end_lng = float(request.form.get("end_lng"))

    # 거리 계산 (haversine formula)
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # radius of Earth in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    distance_m = haversine(start_lat, start_lng, end_lat, end_lng)
    distance_km = round(distance_m / 1000, 2)

    # 표준 속도 기준 보정 시간 (1.4 m/s)
    corrected_time = round(distance_m / 1.4 / 60, 1)

    return render_template_string(result_template,
                                  user=user_name,
                                  input_time=walk_time,
                                  corrected_time=corrected_time,
                                  distance_km=distance_km)

if __name__ == '__main__':
    app.run(debug=True)
