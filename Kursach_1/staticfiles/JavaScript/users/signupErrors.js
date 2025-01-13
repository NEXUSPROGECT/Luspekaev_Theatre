document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
        "X-Requested-With": "XMLHttpRequest",
        },
    });


    if (!response.ok) {
        const data = await response.json();



        if (!data.success) {
            // Обработка ошибок формы
            if (data.errors.non_field_errors) {
                showAlert(data.errors.non_field_errors, "#ff4d4d");
            }
            if (data.errors.field_errors) {
                Object.entries(data.errors.field_errors).forEach(([field, errors]) => {
                    const errorMessage = errors.join(", ");
                    showAlert(`${errorMessage}`, "#ff4d4d");
                });
            }

        }
    } else {
          showAlert(message, "#7DDA58");
          setTimeout(() => {
                window.location.href = href;
            }, 3000); // 2000 миллисекунд = 2 секунды
        }

});
