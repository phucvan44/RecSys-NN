$(document).ready(() => {
    var get_parameters = () => {
        let url = window.location.search.substring(1);
        url = url.split("&")
        let params = {}
        url.forEach(str => {
            str = str.split("=")
            params[str[0]] = str[1]
        });
        return params
    }
    
    var params = get_parameters()
    if("lang" in params){
        $.ajax({
            url:"http://127.0.0.1:5000/movies/languages/"+params["lang"],
            type:"GET",
            success : (data) =>{
                if("Error" in data){
                    window.location.href = "./movies.html?page=1";
                }
                var movies = data["movies"];
                var base_movies = "";
                for(var i = 0; i < movies.length; i+=1){
                    var view = Object.values(movies[i].bar)
                    view = view.reduce((a, b) => a+b, 0)
                    view = view.toLocaleString()
                    base_movies += `
                        <div class="col-md-3">
                            <a href="${movies[i].url}">
                                <div id ="item">
                                    <img src="${movies[i].img}" />
                                    <div>
                                        <p id="title">${movies[i].title}</p>
                                        <p id="view">${view} lượt xem</p>
                                    </div>
                                </div>
                            </a>
                        </div>
                    `
                }
                $(".movie-list #movie").append(base_movies)

                
                var genres = JSON.parse(window.localStorage.getItem("genres"))
                var base_genres = "";
                for(var i = 0; i < genres.length; i+=1){
                    base_genres += `
                        <li><a href="${genres[i].url}"><button>${genres[i].value}</button></a></li>
                    `
                }
                $(".list-tag ul ").append(base_genres)
            }
        });
    }

})