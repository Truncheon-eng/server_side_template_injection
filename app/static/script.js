window.onload = function()  {
    object_container = document.querySelector(".object-container")
    const params = new URLSearchParams({
        name: "Мария",
        age: 26,
        description: "Хороший руководитель с многолетним стажем"
    })
    fetch(`/get_user_info?${params}`).then(response => {
        if (response.ok) {
            return response.text()
        }
    }).then(response => {
        object_container.insertAdjacentHTML("beforeend", response)
    })
}
