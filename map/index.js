  document.addEventListener('DOMContentLoaded', () => {
    const regions = document.querySelectorAll('.region');
    const tooltip = document.getElementById('tooltip');

    // Add this at the top of your file
    const regionMappings = {
      "Черкаська область": "UA-03",
      "Харківська область": "UA-09",
      "Хмельницька область": "UA-11",
      "Київ": "UA-12",
      "Київська область": "UA-13",
      "Миколаївська область": "UA-17",
      "Одеська область": "UA-18",
      "Житомирська область": "UA-27"
      // Add other regions here...
    };

    function getRegionIdFromMapping(regionName) {
      const normalizedRegionName = regionName.trim().toLowerCase();
      for (const [key, value] of Object.entries(regionMappings)) {
        if (key.toLowerCase() === normalizedRegionName) {
          return value;
        }
      }
      console.warn(`Region not found in mappings: ${regionName}`);
      return 'Unknown';
    }

    async function fetchNewsData() {
      console.log("Extracting data from server");
      try {
        const [regionResponse, requestsResponse] = await Promise.all([
          fetch('http://localhost:8000/v1/region_info'),
          fetch('http://localhost:8000/v1/requests_info')
        ]);
    
        if (!regionResponse.ok || !requestsResponse.ok) {
          throw new Error('Failed to fetch data');
        }
    
        const regionData = await regionResponse.json();
        console.log("Region data:", regionData);
        const requestsData = await requestsResponse.json();
        console.log("Requests data:", requestsData);
    
        // Create a map to store merged data by city
        const mergedDataMap = new Map();
    
        // Process region data
        regionData.forEach(region => {
          const existingData = mergedDataMap.get(region.city) || {
            explosions: 0,
            destruction: false,
            casualties: 0,
            housing: 0,
            infrastructure: 0,
            food: 0,
            clothing: 0,
            medicine: 0,
            region: ''
          };
    
          mergedDataMap.set(region.city, {
            ...existingData,
            explosions: existingData.explosions + (region.num_of_explosions || 0),
            destruction: existingData.destruction || region.damage,
            casualties: existingData.casualties + (region.num_of_victims || 0)
          });
        });
    
        // Process requests data
        requestsData.forEach(request => {
          const cityData = mergedDataMap.get(request.city) || {
            explosions: 0,
            destruction: false,
            casualties: 0,
            housing: 0,
            infrastructure: 0,
            food: 0,
            clothing: 0,
            medicine: 0,
            region: ''
          };
    
          // Map region name to SVG ID using the new function
          cityData.region = getRegionIdFromMapping(request.region);
    
          // Increment the appropriate category
          switch (request.category) {
            case 'Відбудова житлових будинків🏡':
              cityData.housing++;
              break;
            case 'Відбудова критичної інфраструктури🏥':
              cityData.infrastructure++;
              break;
            case 'Їжа та продовольчі товари🍎':
              cityData.food++;
              break;
            case 'Одяг👕':
              cityData.clothing++;
              break;
            case 'Медикаменти та засоби особистої гігієни💊':
              cityData.medicine++;
              break;
          }
    
          mergedDataMap.set(request.city, cityData);
        });
    
        // Convert the map to an array
        const mergedData = Array.from(mergedDataMap.values());
        console.log("Merged data:", mergedData);
        return mergedData;
      } catch (error) {
        console.error('Error fetching news data:', error);
        return [];
      }
    }
    
    function updateMap(newsData) {
      regions.forEach(region => {
        const regionId = region.id;
        const regionData = newsData.find(item => item.region === regionId) || {};
        const explosions = regionData.explosions || 0;
        const destruction = regionData.destruction || false;
        const casualties = regionData.casualties || 0;
        const housing = regionData.housing || 0;
        const infrastructure = regionData.infrastructure || 0;
        const food = regionData.food || 0;
        const clothing = regionData.clothing || 0;
        const medicine = regionData.medicine || 0;

        const helpRequests = housing + infrastructure + food + clothing + medicine;

        const color = getColorBasedOnExplosions(explosions);
        region.style.fill = color;

        region.addEventListener('mousemove', (event) => {
          tooltip.style.display = 'block';
          tooltip.style.left = event.pageX + 10 + 'px';
          tooltip.style.top = event.pageY + 10 + 'px';

          tooltip.innerHTML = `
            <strong>Кількість вибухів:</strong> ${explosions}<br>
            <strong>Зруйновані будівлі:</strong> ${destruction ? 'Так' : 'Ні'}<br>
            <strong>Кількість жертв:</strong> ${casualties}<br>
            <strong>Запити допомоги:</strong> ${helpRequests}<br>
            <ul>
              <li>Відбудова житлових будинків: ${housing}</li>
              <li>Відбудова критичної інфраструктури: ${infrastructure}</li>
              <li>Їжа та продовольчі товари: ${food}</li>
              <li>Одяг: ${clothing}</li>
              <li>Медикаменти та засоби особистої гігієни: ${medicine}</li>
            </ul>
          `;
        });

        region.addEventListener('mouseleave', () => {
          tooltip.style.display = 'none';
        });

        if (destruction) {
          addExclamationMarker(region, '!');
        }

        if (casualties > 0) {
          addExclamationMarker(region, '!!', casualties);
        }

        const classifications = { housing, infrastructure, food, clothing, medicine };
        if (Object.values(classifications).some(value => value > 0)) {
          addHelpRequestMarkers(region, classifications);
        }
      });
    }

    // Initial fetch
    fetchNewsData().then(updateMap);

    // Set up interval for periodic updates
    setInterval(() => {
      fetchNewsData().then(updateMap);
    }, 5000); // 5000 milliseconds = 5 seconds
  });

  function getColorBasedOnExplosions(explosions) {
    const maxExplosions = 20;
    const intensity = Math.min(explosions / maxExplosions, 1);
    const yellow = Math.floor(255 * intensity);
    return `rgb(${yellow}, ${yellow}, 100)`;
  }

  function addExclamationMarker(region, symbol, casualties = null) {
    const marker = document.createElement('div');
    marker.className = 'exclamation-marker';
    marker.textContent = symbol;
    marker.style.position = 'absolute';

    const regionRect = region.getBoundingClientRect();
    marker.style.left = regionRect.left + regionRect.width / 2 - 10 + 'px';
    marker.style.top = regionRect.top + regionRect.height / 2 - 10 + 'px';

    marker.style.color = 'blue';
    marker.style.fontWeight = 'bold';

    if (casualties !== null) {
      marker.addEventListener('mouseenter', () => {
        tooltip.style.display = 'block';
        tooltip.textContent = `Кількість жертв: ${casualties}`;
      });

      marker.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
      });
    }

    document.body.appendChild(marker);
  }

  function addHelpRequestMarkers(region, classifications) {
    const markerData = [
      { label: 'Відбудова житлових будинків', value: classifications.housing, color: 'blue' },
      { label: 'Відбудова критичної інфраструктури', value: classifications.infrastructure, color: 'green' },
      { label: 'Їжа та продовольчі товари', value: classifications.food, color: 'orange' },
      { label: 'Одяг', value: classifications.clothing, color: 'purple' },
      { label: 'Медикаменти та засоби особистої гігієни', value: classifications.medicine, color: 'red' }
    ];

    markerData.forEach((data, index) => {
      if (data.value > 0) {
        const marker = document.createElement('div');
        marker.className = 'help-request-marker';
        marker.style.position = 'absolute';
        marker.style.width = '10px'; // Розмір точки
        marker.style.height = '10px'; // Розмір точки
        marker.style.borderRadius = '50%'; // Робить точку круглою
        marker.style.backgroundColor = data.color;
        marker.style.cursor = 'pointer'; // Змінює курсор на вказівний

        const regionRect = region.getBoundingClientRect();
        const markerX = Math.random() * (regionRect.width - 100) + regionRect.left;
        const markerY = Math.random() * (regionRect.height - 140) + regionRect.top;

        marker.style.left = markerX + 'px';
        marker.style.top = markerY + 'px';

        marker.addEventListener('mouseenter', () => {
          tooltip.style.display = 'block';
          tooltip.innerHTML = `<p>${data.label}: ${data.value}</p>`;
        });

        marker.addEventListener('mouseleave', () => {
          tooltip.style.display = 'none';
        });

        document.body.appendChild(marker);
      }
    });
  }

