const plotSelect = document.getElementById('classification_plot');
        const nameSelect = document.getElementById('classification_name');
        const cityForm = document.getElementById('city-form');
        const resultDiv = document.getElementById('result');

        plotSelect.addEventListener('change', updateResult);
        nameSelect.addEventListener('change', updateResult);

        function updateResult() {
            const plotValue = plotSelect.value;
            const name = nameSelect.options[nameSelect.selectedIndex].text;

            if (plotValue === 'classification_plot-two') {
                cityForm.style.display = 'none';  
                resultDiv.innerHTML = '';
            } else {
                cityForm.style.display = 'block';  
                resultDiv.innerHTML = `<p>Місто: ${name}</p>`;  
            }
        }

        window.onload = updateResult;