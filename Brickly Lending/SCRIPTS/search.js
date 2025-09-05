function searchProjects() {
        const searchTerm = document.querySelector('.search-input').value.toLowerCase();
        const projects = document.querySelectorAll('.project-item');
        let foundResults = false;

        projects.forEach(project => {
            const title = project.querySelector('h3').textContent.toLowerCase();
            const description = project.querySelector('p').textContent.toLowerCase();

            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                project.style.display = 'flex';
                foundResults = true;
            } else {
                project.style.display = 'none';
            }
        });

        // Показываем сообщение, если ничего не найдено
        const noResultsMessage = document.getElementById('noResultsMessage');
        if (!foundResults && searchTerm.length > 0) {
            if (!noResultsMessage) {
                const message = document.createElement('div');
                message.id = 'noResultsMessage';
                message.textContent = 'Ничего не найдено';
                message.style.textAlign = 'center';
                message.style.fontSize = '1.5em';
                message.style.margin = '40px 0';
                message.style.color = '#666';
                document.querySelector('.projects-grid').appendChild(message);
            }
        } else if (noResultsMessage) {
            noResultsMessage.remove();
        }
    }

    // Обработчики событий
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.querySelector('.search-input');
        const searchButton = document.querySelector('.search-button');

        // Поиск при вводе текста
        searchInput.addEventListener('input', searchProjects);

        // Поиск при клике на кнопку
        searchButton.addEventListener('click', searchProjects);

        // Поиск при нажатии Enter
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchProjects();
            }
        });
    });