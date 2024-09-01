document.addEventListener('DOMContentLoaded', () => {
    // Function to populate filters based on predictor type
    function populateFilters(predictor) {
        fetch(`/data/${predictor}`)
            .then(response => response.json())
            .then(data => {
                const uniqueValues = (key) => [...new Set(data.map(item => item[key]))];

                const filters = {
                    bike: {
                        brand: 'Brand',
                        modelYear: 'Model-Year',
                        gears: 'Gears',
                        topSpeed: 'Top-Speed'
                    },
                    car: {
                        brand: 'brands',
                        modelYear: 'modelYears',
                        topSpeed: 'topSpeeds'
                    },
                    laptop: {
                        brand: 'Brand',
                        type: 'Type',
                        ram: 'RAM',
                        weight: 'Weight',
                        screenSize: 'ScreenSize',
                        screenResolution: 'ScreenResolution',
                        gpu: 'GPU',
                        cpu: 'CPU',
                        hdd: 'HDD',
                        ssd: 'SSD'
                    },
                    mobile: {
                        brand: 'Brand',
                        ram: 'RAM',
                        cpu: 'CPU',
                        ssd: 'SSD',
                        battery: 'Battery'
                    }
                };

                const filterKeys = filters[predictor];
                Object.keys(filterKeys).forEach(key => {
                    const selectElement = document.getElementById(`${predictor}-${key}`);
                    if (selectElement) {
                        const options = uniqueValues(filterKeys[key]);

                        options.forEach(option => {
                            selectElement.add(new Option(option, option));
                        });
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    // Function to handle form submission
    function handleSubmit(predictor) {
        const form = document.getElementById(`${predictor}-form`);
        const predictedPriceElement = document.getElementById(`${predictor}-predicted-price`);

        form.addEventListener('submit', function(event) {
            event.preventDefault();

            if (!form.checkValidity()) {
                alert('Please fill out all required fields correctly.');
                return;
            }

            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            // Special handling for cars to convert mileage
            if (predictor === 'car') {
                const mileageValue = parseFloat(data.mileageValue);
                const mileageUnit = data.mileageUnit;

                if (data.fuelType === 'Petrol') {
                    data.mileage = mileageValue;  // Liters
                } else if (data.fuelType === 'Gas') {
                    data.mileage = mileageValue * 0.264172;  // Convert Gallons to Liters
                } else if (data.fuelType === 'Electric') {
                    data.mileage = mileageValue / 60;  // Convert Minutes to Hours
                }
            }

            fetch(`/predict/${predictor}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                const conversionRate = predictor === 'laptop' || predictor === 'mobile' ? 82 : 1;
                const priceInCurrency = result.price * conversionRate;

                predictedPriceElement.textContent = `Estimated Price: ₹${priceInCurrency.toFixed(2)}`;
            })
            .catch(error => {
                console.error('Error:', error);
                predictedPriceElement.textContent = 'Error predicting price. Please try again.';
            });
        });
    }

    // Function to show tab content based on predictor type
    function showTab(predictor) {
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.style.display = 'none';
        });
        document.getElementById(`${predictor}-tab`).style.display = 'block';
    }

    // Initialize page
    showTab('bike');  // Default tab

    ['bike', 'car', 'laptop', 'mobile'].forEach(predictor => {
        populateFilters(predictor);
        handleSubmit(predictor);
    });
});
