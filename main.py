import os

import streamlit as st
from dotenv import load_dotenv

from air_quality_client import AirQualityClient, format_time
from air_reading import AirReading
from health_risk_analyzer import HealthRiskAnalyzer
from location_history_store import LocationHistoryStore
from validators import is_valid_location_name

st.set_page_config(page_title='Air Quality & Pollution Health Advisor', layout='centered')
st.title('Air Quality & Pollution Health Advisor')

load_dotenv()
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    st.error('Missing GEMINI_API_KEY. Add a .env file with GEMINI_API_KEY=your_key_here')
    st.stop()

client = AirQualityClient()
store = LocationHistoryStore()
analyzer = HealthRiskAnalyzer(GEMINI_API_KEY)

st.sidebar.header('Favourite Locations')
favourites = store.load_favourites()

if favourites:
    for place in favourites:
        st.sidebar.write(f'- {place}')
else:
    st.sidebar.write('No favourites saved yet.')

tab1, tab2, tab3 = st.tabs(['Check a Location', 'Compare Two Locations', 'History'])

with tab1:
    location_input = st.text_input('Enter a location (e.g. Abuja):', key='single_location')

    if st.button('Check Air Quality'):
        if not is_valid_location_name(location_input):
            st.error('Please enter a valid location name (letters and spaces only).')
        else:
            try:
                lat, lon, name = client.get_coordinates(location_input)
                current_data = client.get_current_air_quality(lat, lon)
                forecast_data = client.get_forecast_air_quality(lat, lon)
                cleanest_hour = client.find_cleanest_hour(forecast_data)
                cleanest_active = client.find_cleanest_active_hour(forecast_data)

                reading = AirReading(
                    location=name,
                    latitude=lat,
                    longitude=lon,
                    aqi=current_data['aqi'],
                    pm2_5=current_data['pm2_5'],
                    pm10=current_data['pm10'],
                    ozone=current_data['ozone'],
                    nitrogen_dioxide=current_data['nitrogen_dioxide'],
                )

                with st.spinner('Getting AI health advice...'):
                    advice = analyzer.get_health_advice(reading, cleanest_hour, cleanest_active)

                store.save_reading(reading)

                # streamlit reruns the whole script on every click, so we
                # need session_state to keep the result on screen
                st.session_state['last_reading'] = reading
                st.session_state['last_cleanest_hour'] = cleanest_hour
                st.session_state['last_cleanest_active'] = cleanest_active
                st.session_state['last_advice'] = advice

            except ValueError as e:
                st.error(str(e))
            except ConnectionError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f'Something went wrong: {e}')

    if 'last_reading' in st.session_state:
        reading = st.session_state['last_reading']
        cleanest_hour = st.session_state.get('last_cleanest_hour')
        cleanest_active = st.session_state.get('last_cleanest_active')
        advice = st.session_state.get('last_advice')

        st.subheader(f'Results for {reading.location}')
        st.write(f'**AQI:** {reading.aqi}')
        st.write(f'**PM2.5:** {reading.pm2_5}')
        st.write(f'**PM10:** {reading.pm10}')
        st.write(f'**Ozone:** {reading.ozone}')
        st.write(f'**Nitrogen dioxide:** {reading.nitrogen_dioxide}')

        if cleanest_hour:
            st.write(f"**Cleanest hour today (overall):** {format_time(cleanest_hour['time'])}")

        if cleanest_active:
            st.write(f"**Cleanest hour, 6 AM to 10 PM:** {format_time(cleanest_active['time'])}")

        st.info(advice)

        if st.button('Save as Favourite'):
            store.add_favourite(reading.location)
            st.success(f'{reading.location} added to favourites!')

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        location_a = st.text_input('First location:', key='location_a')
    with col2:
        location_b = st.text_input('Second location:', key='location_b')

    if st.button('Compare'):
        if not is_valid_location_name(location_a) or not is_valid_location_name(location_b):
            st.error('Please enter two valid location names.')
        else:
            try:
                lat_a, lon_a, name_a = client.get_coordinates(location_a)
                data_a = client.get_current_air_quality(lat_a, lon_a)

                lat_b, lon_b, name_b = client.get_coordinates(location_b)
                data_b = client.get_current_air_quality(lat_b, lon_b)

                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.subheader(name_a)
                    st.write(f"AQI: {data_a['aqi']}")
                    st.write(f"PM2.5: {data_a['pm2_5']}")
                with res_col2:
                    st.subheader(name_b)
                    st.write(f"AQI: {data_b['aqi']}")
                    st.write(f"PM2.5: {data_b['pm2_5']}")

                if data_a['aqi'] is not None and data_b['aqi'] is not None:
                    if data_a['aqi'] < data_b['aqi']:
                        st.success(f'{name_a} has cleaner air right now.')
                    elif data_b['aqi'] < data_a['aqi']:
                        st.success(f'{name_b} has cleaner air right now.')
                    else:
                        st.info('Both locations have similar air quality.')

            except ValueError as e:
                st.error(str(e))
            except ConnectionError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f'Something went wrong: {e}')

with tab3:
    st.subheader('Past Readings')
    history = store.load_history()

    if not history:
        st.write('No history saved yet. Check a location first!')
    else:
        for entry in reversed(history):
            st.write(
                f"{entry['location']} — {entry['timestamp']} — "
                f"AQI: {entry['aqi']}, PM2.5: {entry['pm2_5']}"
            )
