
         function updateCheckboxes() {
            const checkboxes = document.querySelectorAll('.book-type');
            let checkedCount = 0;

            checkboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    checkedCount++;
                }
            });
            checkboxes.forEach(checkbox => {
                if (!checkbox.checked) {
                    checkbox.disabled = checkedCount >= 3;
                } else {
                    checkbox.disabled = false;
                }
            });
        }

        function validateForm() {
            const title = document.getElementById("book-title").value.trim();
            const author = document.getElementById("author-name").value.trim();
            const image = document.getElementById("book-image").value.trim();
            const description = document.getElementById("book-description").value.trim();
            const price = document.getElementById("book-price").value;

            const selectedTypes = Array.from(document.querySelectorAll('.book-type:checked'));
            const typesCount = selectedTypes.length;

            if (!title || !author || !image || typesCount === 0 || !description || price <= 0) {
                alert("All fields must be filled out, at least one book type must be selected, and price must be greater than zero.");
                return false;
            }
            return true;
        }
    function previewImage(event) {
        const input = event.target;
        const preview = document.getElementById('image-preview');

        if (input.files && input.files[0]) {
            const reader = new FileReader();

            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };

            reader.readAsDataURL(input.files[0]);
        }
    }
    function validateForm() {
        const title = document.getElementById("book-title").value.trim();
        const author = document.getElementById("author-name").value.trim();
        const image = document.getElementById("book-image").files.length;
        const description = document.getElementById("book-description").value.trim();
        const price = document.getElementById("book-price").value;
        const selectedTypes = Array.from(document.querySelectorAll('.book-type:checked'));
        const typesCount = selectedTypes.length;
        if (!title || !author || image === 0 || typesCount === 0 || !description || price <= 0) {
            alert("All fields must be filled out, at least one book type must be selected, and price must be greater than zero.");
            return false;
        }
        return true;
    }