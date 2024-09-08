  document.addEventListener('DOMContentLoaded', () => {
    const regions = document.querySelectorAll('.region');
    const tooltip = document.getElementById('tooltip');

    fetchNewsData().then(newsData => {
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
    });
  });

  async function fetchNewsData() {
    return [
      {
        region: "UA-9",
        explosions: 15,
        destruction: true,
        casualties: 3,
        housing: 10,
        infrastructure: 8,
        food: 15,
        clothing: 5,
        medicine: 7
      },
      {
        region: "UA-6",
        explosions: 7,
        destruction: true,
        casualties: 0,
        housing: 0,
        infrastructure: 0,
        food: 0,
        clothing: 0,
        medicine: 0
      },
      {
        region: "UA-13",
        explosions: 0,
        destruction: false,
        casualties: 0,
        housing: 2,
        infrastructure: 4,
        food: 0,
        clothing: 0,
        medicine: 3
      }
    ];
  }

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
