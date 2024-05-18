document.addEventListener('DOMContentLoaded', function() {
    var addCourseModal = document.getElementById('addCourseModal');
    var addCourseButton = document.getElementById('add-course');
    var closeButton = document.querySelector('.close');

    // Show modal when Add Course button is clicked
    addCourseButton.addEventListener('click', function() {
        addCourseModal.style.display = 'block';
    });

    // Hide modal when close button is clicked
    closeButton.addEventListener('click', function() {
        addCourseModal.style.display = 'none';
    });

    // Hide modal when user clicks outside the modal
    window.addEventListener('click', function(event) {
        if (event.target === addCourseModal) {
            addCourseModal.style.display = 'none';
        }
    });

    // Delete Course button functionality
    document.getElementById('delete-courses').addEventListener('click', function() {
        var selectedCourses = document.querySelectorAll('input[name="selected_courses"]:checked');
        if (selectedCourses.length === 0) {
            alert('Please select at least one course to delete.');
        } else {
            var confirmation = confirm('Are you sure you want to delete the selected courses?');
            if (confirmation) {
                var courseIds = [];
                selectedCourses.forEach(function(course) {
                    courseIds.push(course.value);
                });

                // Send AJAX request to delete courses
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/delete-courses/', true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        // Handle successful deletion
                        alert('Courses deleted successfully.');
                        // You may want to reload the page or update the UI accordingly
                    } else {
                        // Handle error
                        alert('Failed to delete courses. Please try again.');
                    }
                };
                xhr.send(JSON.stringify({ courseIds: courseIds }));
            }
        }
    });

    // Add Course form submission
    document.getElementById('addCourseForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(this);

        // Send AJAX request to add course
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/add-course/', true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Handle successful addition
                alert('Course added successfully.');
                // You may want to reload the page or update the UI accordingly
            } else {
                // Handle error
                alert('Failed to add course. Please try again.');
            }
        };
        xhr.send(formData);
    });
});
