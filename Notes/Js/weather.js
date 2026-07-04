
// WEATHER COMPONENTS


// VARIABLES

const cityTitle = document.getElementById('heading-city');
const searchCity = document.getElementById('search-city');
const searchBtnCity = document.getElementById('search-btn');


const h2Weather = document.getElementById('h2-weather');
const pWeather = document.getElementById('paragraph-weather');
const h2Wind = document.getElementById('h2-wind');
const pWind = document.getElementById('paragraph-wind');
const h2Temperature = document.getElementById('h2-temperature');
const pTemperature = document.getElementById('paragraph-temperature');
const h2Time = document.getElementById('h2-time');
const pTime = document.getElementById('paragraph-time');


const weatherBtn = document.getElementById('weather-btn');
const windBtn = document.getElementById('wind-btn');
const temperatureBtn = document.getElementById('temperature-btn');
const timeBtn = document.getElementById('time-btn');


const weatherContentBox = document.getElementById('weather-description');
const windBox = document.getElementById('wind-content');
const temperatureBox = document.getElementById('temperature-content');
const timeBox = document.getElementById('time-content');


navigator.geolocation.getCurrentPosition(
    async function(position) {
        try {
            windBox.style.display = 'none';
            temperatureBox.style.display = 'none';
            timeBox.style.display = 'none';
            weatherContentBox.style.display = 'block';

            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            console.log("Coordinates:", lat, lon);
            
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`);
            const data = await response.json();
            let city = data.address.city || data.address.town || data.address.village || data.address.suburb || "Unknown Location";
            
            cityTitle.innerText = city;
            
            const dataResponse = await fetch(
                `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&timezone=auto`
            );
            
            console.log("Response OK:", dataResponse.ok);
            
            if (!dataResponse.ok) {
                const error = await dataResponse.text();
                console.error("API Error:", error);
                return;
            }
            
            const weather = await dataResponse.json();
            const weatherCodeNum = weather.current_weather?.weathercode;
            
            const result = getWeatherDescription(weatherCodeNum);
            h2Weather.innerText = `The Weather Condition here in the ${city} City.`;
            pWeather.innerText = result;

            const windSpeed = weather.current_weather?.windspeed;
            h2Wind.innerText = `The WindSpeed Condition here in ${city}`;
            pWind.innerText = `The WindSpeed is ${windSpeed}`;

            const temperature = weather.current_weather.temperature;
            h2Temperature.innerText = `The Temperature Condition her in the ${city} City`;
            pTemperature.innerText = getTemperatureDescription(temperature);

            const currentTime = weather.current_weather.time;
            h2Time.innerText = `The Current Time in the ${city} City`;
            const timeObject = new Date(currentTime);
            const formattedTime = timeObject.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: true
            });
            pTime.innerText = formattedTime;

        } catch (error) {
            console.log("Error:", error);
        }
    },
    function(error) {
        cityTitle.innerText = 'Search for a city';
    }
)



async function getCoordinates(cityName) {

    try {

        const response = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${cityName}&count=1&language=en&format=json`);
        const position = await response.json();
        return position;

    } catch (error) {
        console.log(error);
    }

}

async function getWeather(position) {

    try {
        const latitude = position.results[0].latitude;
        const longitude = position.results[0].longitude;
        const response = await fetch(
            `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true&timezone=auto`
        );
        const weather = await response.json();
        return weather;
    } catch (error) {
        console.log(error);
    }

}

function getTemperatureDescription(temperature) {
    
    // HOT TEMPERATURES
    if (temperature >= 35) {
        return "It's extremely hot out there! Stay cool and hydrated!";
    }
    
    if (temperature >= 30 && temperature < 35) {
        return "It's very hot today - wear light clothes and stay in the shade!";
    }
    
    if (temperature >= 25 && temperature < 30) {
        return "It's warm and comfortable today - perfect for outdoor activities!";
    }
    
    // WARM TEMPERATURES
    if (temperature >= 20 && temperature < 25) {
        return "It's a pleasant warm day - nice weather overall!";
    }
    
    if (temperature >= 15 && temperature < 20) {
        return "It's slightly warm - a light jacket might be comfortable!";
    }
    
    // COOL TEMPERATURES
    if (temperature >= 10 && temperature < 15) {
        return "It's cool today - bring a sweater or light jacket!";
    }
    
    if (temperature >= 5 && temperature < 10) {
        return "It's chilly out there - wear a warm jacket!";
    }
    
    // COLD TEMPERATURES
    if (temperature >= 0 && temperature < 5) {
        return "It's cold today - bundle up with layers!";
    }
    
    if (temperature >= -5 && temperature < 0) {
        return "It's very cold! Keep warm and avoid going out too long!";
    }
    
    // VERY COLD TEMPERATURES
    if (temperature >= -10 && temperature < -5) {
        return "It's extremely cold - stay indoors if possible!";
    }
    
    if (temperature < -10) {
        return "Dangerously cold temperatures! Stay inside and keep warm!";
    }
    
    return "Temperature information unavailable.";
}

function getWeatherDescription(weatherCode) {

    const staticWeather = {
        0: "The sky is clear and sunny today!",
        1: "It's mostly clear with a few clouds scattered around.",
        2: "Partly cloudy skies with sun peeking through the clouds.",
        3: "The sky is completely covered with clouds today."
    };

    if (staticWeather[weatherCode] !== undefined) {
        return staticWeather[weatherCode];
    }

    // 2. Handle ranges and specific codes cleanly
    if (weatherCode >= 45 && weatherCode <= 48) {
        return "Foggy conditions - visibility is low today.";
    }
    
    if (weatherCode >= 51 && weatherCode <= 57) {
        if (weatherCode >= 56) return "Freezing drizzle - cold rain freezing on surfaces!";
        if (weatherCode === 55) return "Dense drizzle - steady light rain covering everything.";
        if (weatherCode === 53) return "Moderate drizzle - consistent light rain falling.";
        return "Light drizzle falling - a gentle misty rain.";
    }

    if (weatherCode >= 61 && weatherCode <= 67) {
        if (weatherCode >= 66) return "Freezing rain - dangerous icy rain conditions!";
        if (weatherCode === 65) return "Heavy rain - strong rainfall, bring your umbrella!";
        if (weatherCode === 63) return "Moderate rain - steady rainfall continuing.";
        return "Light rain falling - a gentle shower today.";
    }

    if (weatherCode >= 71 && weatherCode <= 77) {
        if (weatherCode === 77) return "Snow grains - tiny ice crystals falling like snow.";
        if (weatherCode === 75) return "Heavy snow - strong snowfall today!";
        if (weatherCode === 73) return "Moderate snow - steady snowfall continuing.";
        return "Light snow falling - gentle snowflakes drift down.";
    }

    if (weatherCode >= 80 && weatherCode <= 82) {
        if (weatherCode === 82) return "Violent rain showers - intense rain bursts!";
        if (weatherCode === 81) return "Moderate rain showers - regular bursts of rain.";
        return "Light rain showers - brief periods of light rain.";
    }

    if (weatherCode >= 85 && weatherCode <= 86) {
        if (weatherCode === 86) return "Heavy snow showers - strong snow bursts!";
        return "Light snow showers - brief snow flurries.";
    }

    if (weatherCode >= 95 && weatherCode <= 99) {
        if (weatherCode === 99) return "Thunderstorm with heavy hail - dangerous!";
        if (weatherCode === 96) return "Thunderstorm with light hail - thunder and lightning!";
        return "Thunderstorm approaching - thunder and lightning out there!";
    }

    return "Weather conditions unknown.";
}


searchBtnCity.addEventListener('click', async () => {

    try {
        let city = searchCity.value;

        if (city !== undefined) {
            const position = await getCoordinates(city);
            console.log(position);
            
            const weather = await getWeather(position);
            const weatherCodeNum = weather.current_weather?.weathercode;
            const result = getWeatherDescription(weatherCodeNum);
            cityTitle.innerText = city;
            h2Weather.innerText = `The Weather Condition here in the ${city} City.`;
            pWeather.innerText = result;

            const windSpeed = weather.current_weather?.windspeed;
            h2Wind.innerText = `The WindSpeed Condition here in ${city}`;
            pWind.innerText = `The WindSpeed is ${windSpeed}`;

            const temperature = weather.current_weather.temperature;
            h2Temperature.innerText = `The Temperature Condition her in the ${city} City`;
            pTemperature.innerText = getTemperatureDescription(temperature);

            const currentTime = weather.current_weather.time;
            h2Time.innerText = `The Current Time in the ${city} City`;
            const timeObject = new Date(currentTime);
            const formattedTime = timeObject.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: true
            });
            pTime.innerText = formattedTime;
        } else {
            cityTitle.innerText = 'Unknown City';
        }
    } catch (error) {
        console.log(error);
    }

});

weatherBtn.addEventListener('click', () => {

    windBox.style.display = 'none';
    temperatureBox.style.display = 'none';
    timeBox.style.display = 'none';
    weatherContentBox.style.display = 'block';

});

windBtn.addEventListener('click', () => {

    windBox.style.display = 'block';
    temperatureBox.style.display = 'none';
    timeBox.style.display = 'none';
    weatherContentBox.style.display = 'none';

});

temperatureBtn.addEventListener('click', () => {

    windBox.style.display = 'none';
    temperatureBox.style.display = 'block';
    timeBox.style.display = 'none';
    weatherContentBox.style.display = 'none';

});

timeBtn.addEventListener('click', () => {

    windBox.style.display = 'none';
    temperatureBox.style.display = 'none';
    timeBox.style.display = 'block';
    weatherContentBox.style.display = 'none';

});

