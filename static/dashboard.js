document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    if (file) {
        var formData = new FormData();
        formData.append('image', file);

        // Replace 'your-server-endpoint' with your actual server endpoint
        fetch('your-server-endpoint', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Image uploaded successfully!');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Image upload failed!');
        });
    } else {
        alert('Please select an image to upload.');
    }
});

function fetchMedicalNews() {
    // Replace 'your-news-api-endpoint' with your actual news API endpoint
    fetch('https://newsapi.org/v2/everything?q=medical&apiKey=65b4d6638b5e4fe0b7e30f0655b98f14') // Use a valid API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Medical News Data:', data); // Log the fetched data
            var newsContent = document.getElementById('news-content');
            newsContent.innerHTML = ''; // Clear any existing content
            if (data.articles && data.articles.length > 0) {
                data.articles.forEach(article => {
                    var articleElement = document.createElement('div');
                    articleElement.className = 'news-article';
                    articleElement.innerHTML = `
                        <h4>${article.title}</h4>
                        <p>${article.description}</p>
                        <a href="${article.url}" target="_blank">Read more</a>
                    `;
                    newsContent.appendChild(articleElement);
                });

                // Call the function to start auto-scrolling after news is loaded
                startAutoScroll(newsContent);
            } else {
                newsContent.innerHTML = '<p>No news articles found.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching news:', error);
        });
}

function startAutoScroll(element) {
    const scrollHeight = element.scrollHeight;
    const clientHeight = element.clientHeight;
    let scrollTop = 0;
    let direction = 1; // 1 means scrolling down, -1 means scrolling up

    setInterval(() => {
        scrollTop += direction;
        if (scrollTop + clientHeight >= scrollHeight) {
            direction = -1;
        } else if (scrollTop <= 0) {
            direction = 1;
        }
        element.scrollTop = scrollTop;
    }, 50); // Adjust the interval to control the speed of scrolling
}

// Call the function to fetch and display medical news
fetchMedicalNews();
let slideIndex = 0;
showSlides();

function showSlides() {
    let slides = document.getElementsByClassName("slide");
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}    
    slides[slideIndex-1].style.display = "block";  
    setTimeout(showSlides, 3000); // Change image every 3 seconds
}
