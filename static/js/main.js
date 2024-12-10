// Pricing Calculator
document.addEventListener('DOMContentLoaded', function() {
    const calculator = document.getElementById('pricing-calculator');
    if (calculator) {
        calculator.addEventListener('change', calculatePrice);
    }

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});

function calculatePrice() {
    const service = document.getElementById('service-type').value;
    const hosting = document.getElementById('hosting').checked;
    const complexity = document.getElementById('complexity').value;
    
    let basePrice = 0;
    let hostingPrice = 0;
    let serviceName = '';

    // Calculate base price and service name
    switch(service) {
        case 'discord-bot':
            serviceName = 'Discord Bot';
            switch(complexity) {
                case 'starter': basePrice = 0; break;
                case 'hobbyist': basePrice = 5; break;
                case 'professional': basePrice = 15; break;
            }
            hostingPrice = hosting ? 10 : 0; // $10/month for hosting
            break;
        case 'discord-server':
            serviceName = 'Discord Server';
            switch(complexity) {
                case 'starter': basePrice = 3; break;
                case 'hobbyist': basePrice = 5; break;
                case 'professional': basePrice = 10; break;
            }
            hostingPrice = hosting ? 10 : 0; // $10/month for hosting
            break;
        case 'minecraft-server':
            serviceName = 'Minecraft Server';
            switch(complexity) {
                case 'starter': basePrice = 10; break;
                case 'hobbyist': basePrice = 15; break;
                case 'professional': basePrice = 20; break;
            }
            hostingPrice = hosting ? 10 : 0; // $10/month for hosting
            break;
    }

    // Display results
    document.getElementById('base-price').textContent = `$${basePrice}`;
    document.getElementById('hosting-price').textContent = hosting ? 
        `$${hostingPrice}/month` : '$0';
    document.getElementById('total-price').textContent = 
        hosting ? `$${basePrice} and $${hostingPrice}/month` : `$${basePrice}`;
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
