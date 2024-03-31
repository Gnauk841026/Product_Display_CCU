
var selectBox = document.getElementById("type");


selectBox.addEventListener("change", function() {

    var selectedOption = document.querySelector(".selected");
    if (selectedOption) {
        selectedOption.classList.remove("selected");
    }

    // 將新選中的項目添加樣式
    var selectedValue = this.value;
    var selectedOption = document.querySelector("option[value='" + selectedValue + "']");
    selectedOption.classList.add("selected");
});



function performSearch() {
    console.log("執行搜索操作");
    // 从这里开始，是您原先定义的 performSearch 的逻辑
    const date = document.getElementById('price_min').value;
    const name = document.getElementById('price_max').value;
    const typeSelect = document.getElementById('type');
    const platform = typeSelect.value; // 直接使用选中的值

    // 根据选择的平台调整查询参数
    let platformQueryParam = '';
    if(platform === 'type_true') {
        platformQueryParam = 'Pchome';
    } else if(platform === 'type_false') {
        platformQueryParam = 'momo';
    }

    let apiUrl = `http://127.0.0.1:10101/users?platform=${platformQueryParam}`;
    if (name) {
        apiUrl += `&name=${name}`;
    }
    if (date) {
        apiUrl += `&date=${date}`;
    }

    fetch(apiUrl)
    .then(response => response.json())
    .then(result => {
        const tableBody = document.querySelector(".scrollable-table tbody");
        tableBody.innerHTML = ''; // 清空表格当前内容
        if (result.data && result.data.length > 0) {
            result.data.forEach(product => {
                const row = tableBody.insertRow();
                row.insertCell(0).textContent = product.date;
                row.insertCell(1).textContent = product.time;
                row.insertCell(2).textContent = product.name;
                row.insertCell(3).textContent = product.discount;
                row.insertCell(4).textContent = product.price;
            });
        } else {
            const row = tableBody.insertRow();
            const cell = row.insertCell(0);
            cell.textContent = '未找到商品。';
            cell.colSpan = 5;
        }
    })
    .catch(error => {
        console.error('获取商品数据时出错:', error);
    });
}
    
function initPage() {
    // 设置默认值为Momo并查询
    document.getElementById('type').value = "type_false";
    performSearch(); // 这里不需要传递参数
}

window.onload = initPage;


document.addEventListener("DOMContentLoaded", function() {
    var tableContainer = document.querySelector(".scrollable-table-container");
    var computedStyles = window.getComputedStyle(tableContainer);
    if (tableContainer.scrollHeight > tableContainer.clientHeight) {
        tableContainer.classList.add("overflow-visible");
    }
});
