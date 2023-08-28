def balloon_report_template(
    drone_no,
    flight_date, 
    f_time, 
    batt_cons, 
    photos, 
    photos_fb,
    motors,
    motors_fb,
    trigger,
    trig_fb,
    imu,
    imu_fb,
    vcc,
    vcc_fb,
    gps,
    gps_fb
    ):
    html = f"""<html>
    <table border="0" cellpadding="0" cellspacing="0" style="width:500px">
	<tbody>
		<tr>
			<td>
			<p><span style="font-size:18px"><strong>Drone UID: </strong>{drone_no}</span><br />
			<span style="font-size:18px"><strong>Flight date:</strong> {flight_date.date()}</span><br />
			<span style="font-size:18px"><strong>Flight time:</strong> {f_time}</span><br />
			<span style="font-size:18px"><strong>Battery usage:</strong> {batt_cons}</span></p>
			</td>
		</tr>
		<tr>
			<td>
			<table border="1" cellpadding="0" cellspacing="1" style="border-radius:25px; border:1px solid white; width:100%">
				<tbody>
					<tr>
						<td style="background-color:#eeeeee; width:50%">
						<p style="text-align:center"><span style="font-size:20px">📸 <strong>Photos</strong></span></p>

						<p style="text-align:center"><span style="font-size:20px">{photos}</span><br />
						<span style="font-size:18px">{photos_fb}</span></p>
						</td>
						<td style="background-color:#eeeeee; width:50%">
						<p style="text-align:center"><span style="font-size:20px">⚙️ <strong>Motors</strong></span></p>

						<p style="text-align:center"><span style="font-size:20px">{motors}</span><br />
						<span style="font-size:18px">{motors_fb}</span></p>
						</td>
					</tr>
					<tr>
						<td style="background-color:#eeeeee; width:50%">
						<p style="text-align:center"><span style="font-size:20px">💥 <strong>Triggers</strong></span></p>

						<p style="text-align:center"><span style="font-size:20px">{trigger}</span><br />
						<span style="font-size:18px">{trig_fb}</span></p>
						</td>
						<td style="background-color:#eeeeee; width:50%">
						<p style="text-align:center"><span style="font-size:20px">👋 <strong>IMU</strong></span></p>

						<p style="text-align:center"><span style="font-size:20px">{imu}</span><br />
						<span style="font-size:18px">{imu_fb}</span></p>
						</td>
					</tr>
					<tr>
						<td style="background-color:#eeeeee; width:50%">
						<p style="text-align:center"><span style="font-size:20px">🌐 <strong>GPS / Logger</strong></span></p>

						<p style="text-align:center"><span style="font-size:20px">{gps}</span><br />
						<span style="font-size:18px">{gps_fb}</span></p>
						</td>
						<td style="background-color:#eeeeee; width:50%">
						<p style="text-align:center"><span style="font-size:20px">⚡ <strong>Vcc</strong></span></p>

						<p style="text-align:center"><span style="font-size:20px">{vcc}</span><br />
						<span style="font-size:18px">{vcc_fb}</span></p>
						</td>
					</tr>
				</tbody>
			</table>
			</td>
		</tr>
	</tbody>
</table>
</html>"""
    return html