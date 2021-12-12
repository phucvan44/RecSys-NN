$(document).ready(() => {
    $.ajax({
        url:"http://127.0.0.1:5000/navbar",
        type:"GET",
        success : (data) =>{
            window.localStorage.setItem("genres", JSON.stringify(data.genres))
            var languages = "";
            for(var i = 0; i < data.languages.length; i+=1){
                languages += `<li><a href="${data.languages[i].url}">${data.languages[i].value}</a></li>`
            }

            var genres = "";
            for(var i = 0; i < data.genres.length; i+=1){
                genres += `<li><a href="${data.genres[i].url}">${data.genres[i].value}</a></li>`
            }
            
            $(".nav-top #qg ul").append(languages)
            $(".nav-top #gen ul").append(genres)
        }
    });
})