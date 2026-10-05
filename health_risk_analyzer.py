import google.generativeai as genai

from air_quality_client import format_time


class HealthRiskAnalyzer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3.6-flash')

    def build_prompt(self, reading, cleanest_hour=None, cleanest_active_hour=None):
        prompt = (
            f"The air quality in {reading.location} right now is:\n"
            f"- US AQI: {reading.aqi}\n"
            f"- PM2.5: {reading.pm2_5}\n"
            f"- PM10: {reading.pm10}\n"
            f"- Ozone: {reading.ozone}\n"
            f"- Nitrogen dioxide: {reading.nitrogen_dioxide}\n\n"
            "Explain in simple everyday language what these numbers mean. "
            "Say clearly if it's safe to be outside right now, especially for "
            "kids, elderly people and people with asthma or breathing issues. "
            "Then give 2-3 short protective tips (mask, closing windows, air "
            "purifier etc) if needed. Keep it to about 5-6 sentences, no "
            "headings or bullet points." 
        )

        if cleanest_hour is not None and cleanest_active_hour is not None:
            if cleanest_hour['time'] == cleanest_active_hour['time']:
                # the cleanest hour is already a normal waking hour
                prompt += f"\nAlso mention the cleanest time today looks like around {format_time(cleanest_hour['time'])}."
            else:
                prompt += (
                    f"\nThe cleanest hour of the whole day is {format_time(cleanest_hour['time'])}, "
                    "but that is outside the hours most people are out and about. Mention that briefly, "
                    "then say the cleanest time during normal waking hours (6 AM to 10 PM) is around "
                    f"{format_time(cleanest_active_hour['time'])} and recommend that time for outdoor activity."
                )
        elif cleanest_hour is not None:
            prompt += f"\nAlso mention the cleanest time today looks like around {format_time(cleanest_hour['time'])}."

        return prompt

    def get_health_advice(self, reading, cleanest_hour=None, cleanest_active_hour=None):
        prompt = self.build_prompt(reading, cleanest_hour, cleanest_active_hour)

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return (
                f"Sorry, could not get AI advice right now ({e}). "
                "Check the raw numbers above and be careful if the AQI looks high."
            )
