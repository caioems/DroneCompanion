f'''
<html>
<table align="center" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse; height:270px; width:400px">
<tbody>
	<tr>
		<td>
		<table align="center" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse; height:100%; margin-left:auto; margin-right:auto; opacity:0.95; width:100%">
			<tbody>
				<tr>
					<td style="height:90px; text-align:center; vertical-align:middle; width:50%">
					<p><span style="color:#000000"><strong><span style="font-family:Tahoma,Geneva,sans-serif">Flight time:</span></strong></span></p>

					<p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{str(flight_time.components.minutes)}m {str(flight_time.components.seconds)}s</span></strong></span></p>
					</td>
					<td style="height:90px; text-align:center; vertical-align:middle; width:50%">
					<p><span style="color:#000000"><strong><span style="font-family:Tahoma,Geneva,sans-serif">Batt. cons.:</span></strong></span></p>

					<p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{str(round(self.df_dict['BAT'].CurrTot[-1]))} mAh</span></strong></span></p>
					</td>
				</tr>
				<tr>
					<td style="height:90px; text-align:center; vertical-align:middle; width:50%">
					<p><span style="color:#000000"><strong><span style="font-family:Tahoma,Geneva,sans-serif">Camera:</span></strong></span></p>

					<p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{self.mdata_test['Result'][0]}</span></strong></span></p>

					<p><span style="color:#bdc3c7"><em><span style="font-family:Tahoma,Geneva,sans-serif">{self.mdata_test['Result'][1]}&nbsp;</span></em></span></p>
					</td>
					<td style="height:90px; text-align:center; vertical-align:middle; width:50%">
					<p><span style="color:#000000"><strong><span style="font-family:Tahoma,Geneva,sans-serif">Motors:</span></strong></span></p>

					<p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.motors_status}</span></strong></span></p>

					<p><span style="color:#bdc3c7"><em><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.motors_feedback}&nbsp;</span></em></span></p>
					</td>
				</tr>
				<tr>
					<td style="height:90px; text-align:center; vertical-align:middle; width:50%">
					<p><span style="color:#000000"><strong><span style="font-family:Tahoma,Geneva,sans-serif">IMU:</span></strong></span></p>

					<p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.imu_status}</span></strong></span></p>

					<p><span style="color:#bdc3c7"><em><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.imu_feedback}</span></em></span></p>

					<p>&nbsp;</p>
					</td>
					<td style="height:90px; text-align:center; vertical-align:middle; width:50%">
					<p><span style="color:#000000"><strong><span style="font-family:Tahoma,Geneva,sans-serif">Board voltage:</span></strong></span></p>

					<p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.vcc_status}</span></strong></span></p>

					<p><span style="color:#bdc3c7"><em><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.vcc_feedback}&nbsp;</span></em></span></p>
					</td>
				</tr>
			</tbody>
		</table>

		<p>&nbsp;</p>
		</td>
		<td>&nbsp;
		<table align="center" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse; height:100%; margin-left:auto; margin-right:auto; width:100%">
			<tbody>
				<tr>
					<td style="height:55px; text-align:center; vertical-align:middle; width:50%"><span style="font-size:24px"><span style="font-family:Tahoma,Geneva,sans-serif"><span style="color:#2ecc71"><strong>{self.report.motors_pwm_list[2]}</strong></span></span></span></td>
					<td style="height:55px; text-align:center; vertical-align:middle; width:50%"><span style="font-size:24px"><span style="font-family:Tahoma,Geneva,sans-serif"><strong><span style="color:#3498db">{self.report.motors_pwm_list[0]}</span></strong></span></span></td>
				</tr>
				<tr>
					<td colspan="2" style="text-align:center; vertical-align:middle"><span style="font-family:Tahoma,Geneva,sans-serif"><img alt="" src="{template_path.as_uri()}" style="border-style:solid; border-width:0px; height:159px; margin-left:20px; margin-right:20px; width:149px" /></span></td>
				</tr>
				<tr>
					<td style="height:55px; text-align:center; vertical-align:middle; width:50%"><span style="font-size:24px"><span style="font-family:Tahoma,Geneva,sans-serif"><strong><span style="color:#3498db">{self.report.motors_pwm_list[1]}</span></strong></span></span></td>
					<td style="height:55px; text-align:center; vertical-align:middle; width:50%"><span style="font-size:24px"><span style="font-family:Tahoma,Geneva,sans-serif"><span style="color:#2ecc71"><strong>{self.report.motors_pwm_list[3]}</strong></span></span></span></td>
				</tr>
			</tbody>
		</table>

		<p>&nbsp;</p>
		</td>
	</tr>
</tbody>
</table>
</html>'''
