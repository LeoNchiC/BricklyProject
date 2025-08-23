    function scrollToAboutUs() {
        const aboutUsSection = document.getElementById('about-us-section');
        if (aboutUsSection) {
            aboutUsSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'     
            });
        }
    }