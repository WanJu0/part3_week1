console.log('loaded')
let file=""
let formData=""
let content=""
const inputElement = document.querySelector("#img");
inputElement.addEventListener('change', (e) => {
file = e.target.files[0]; //取得檔案資訊 資料通常在陣列中第一筆[0]
console.log(file)
// 创建一个包含原文件内容的 Blob

// 如果圖片形式不是image相關的則return false
if (!file.type.match('image.*')) {
    return false;
}
// const reader = new FileReader();
// // FileReader.readAsDataURL()：讀取指定 Blob 中的內容，完成之後，result 屬性中將包含一個data: URL 格式的 Base64 字符串以表示所讀取文件的內容。
// reader.readAsDataURL(file);

formData = new FormData();
formData.append('img', file);
// 取得文字訊息
content = document.querySelector("#content").value;
console.log(content)
formData.append('content', content);


});
function update_photo(){
    console.log(formData)
    fetch("/api/images", {
        method: 'POST',
        body: formData,
    })
    .then((response) => {
        // 這裡會得到一個 ReadableStream 的物件
        // 可以透過 blob(), json(), text() 轉成可用的資訊
        return response.json();
    }).then((jsonData) => {
        console.log(jsonData,"回傳")
        let content=document.querySelector(".donw_content")
        let contentDiv = document.createElement("div");
        contentDiv.className ="message";
        let textDiv = document.createElement("div");
        textDiv.className ="text";
        let textNode = document.createTextNode(jsonData.content);
        textDiv.appendChild(textNode);
        contentDiv.appendChild(textDiv);
        content.prepend(contentDiv);


        let img = document.createElement("img");
        img.src = jsonData.photo;
        // 將圖片放在attraction_content容器下面
        contentDiv.appendChild(img);

    })
}

fetch("/api/images", {
    method: 'GET',
})
.then((response) => {
    // 這裡會得到一個 ReadableStream 的物件
    // 可以透過 blob(), json(), text() 轉成可用的資訊
    return response.json();
}).then((jsonData) => {
    console.log(jsonData,"1111")
    console.log(jsonData.length,"1")
    console.log(jsonData[0].content)
    console.log(jsonData[0].photo)
    for(let i=0;i<jsonData.length;i++){
        let content=document.querySelector(".donw_content")
    // 
        let contentDiv = document.createElement("div");
        contentDiv.className ="message";
        let textDiv = document.createElement("div");
        textDiv.className ="text";
        let textNode = document.createTextNode(jsonData[i].content);
        textDiv.appendChild(textNode);
        contentDiv.appendChild(textDiv);
        content.prepend(contentDiv);

        let img = document.createElement("img");
        img.src = jsonData[i].photo;
        // 將圖片放在attraction_content容器下面
        contentDiv.appendChild(img);
    }

})